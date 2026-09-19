#ifndef COUNTERS_LINUX_PERF_EVENTS_H_
#define COUNTERS_LINUX_PERF_EVENTS_H_
#ifdef __linux__

#include <asm/unistd.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <cerrno>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

namespace counters {

template <int TYPE = PERF_TYPE_HARDWARE>
class LinuxEvents {
  int fd{-1};
  bool working{false};
  bool last_read_scheduled{false};
  perf_event_attr attribs{};
  size_t num_events{};
  std::vector<uint64_t> temp_result_vec{};
  std::vector<uint64_t> ids{};
  std::vector<int> all_fds{};

public:
  explicit LinuxEvents(std::vector<int> config_vec) {
    std::vector<int> current_configs = config_vec;

    while (!current_configs.empty()) {
      if (!try_open(current_configs)) {
        cleanup_fds();
        current_configs.pop_back();
        continue;
      }

      if (probe_scheduling()) {
        working = true;
        num_events = current_configs.size();
        return;
      }

      cleanup_fds();
      current_configs.pop_back();
    }
  }

  ~LinuxEvents() { cleanup_fds(); }

  inline void start() {
    if (fd != -1) {
      if (ioctl(fd, PERF_EVENT_IOC_RESET, PERF_IOC_FLAG_GROUP) == -1) {
        report_error("ioctl(PERF_EVENT_IOC_RESET)");
      }
      if (ioctl(fd, PERF_EVENT_IOC_ENABLE, PERF_IOC_FLAG_GROUP) == -1) {
        report_error("ioctl(PERF_EVENT_IOC_ENABLE)");
      }
    }
  }

  inline void end(std::vector<unsigned long long> &results) {
    last_read_scheduled = false;
    if (fd == -1) return;

    if (ioctl(fd, PERF_EVENT_IOC_DISABLE, PERF_IOC_FLAG_GROUP) == -1) {
      report_error("ioctl(PERF_EVENT_IOC_DISABLE)");
    }
    if (read(fd, temp_result_vec.data(), temp_result_vec.size() * 8) == -1) {
      report_error("read");
      return;
    }

    // Layout with TOTAL_TIME_ENABLED | TOTAL_TIME_RUNNING | GROUP | ID:
    //   nr, time_enabled, time_running, { value, id } * nr
    uint64_t nr           = temp_result_vec[0];
    uint64_t time_enabled = temp_result_vec[1];
    uint64_t time_running = temp_result_vec[2];

    last_read_scheduled =
        (time_running > 0) && (time_running == time_enabled);

    for (uint64_t i = 0; i < nr; ++i) {
      uint64_t value = temp_result_vec[3 + 2 * i];
      uint64_t id    = temp_result_vec[3 + 2 * i + 1];
      results[i] = value;
      if (ids[i] != id) report_error("event mismatch");
    }
  }

  bool is_working() const { return working; }
  bool last_scheduled() const { return last_read_scheduled; }
  size_t event_count() const { return num_events; }

private:
  bool try_open(const std::vector<int> &configs) {
    working = true;
    fd = -1;
    all_fds.clear();
    num_events = configs.size();
    ids.assign(configs.size(), 0);

    memset(&attribs, 0, sizeof(attribs));
    attribs.type           = TYPE;
    attribs.size           = sizeof(attribs);
    attribs.disabled       = 1;
    attribs.exclude_kernel = 1;
    attribs.exclude_hv     = 1;
    attribs.sample_period  = 0;
    attribs.read_format    = PERF_FORMAT_GROUP
                           | PERF_FORMAT_ID
                           | PERF_FORMAT_TOTAL_TIME_ENABLED
                           | PERF_FORMAT_TOTAL_TIME_RUNNING;

    int group = -1;
    for (size_t i = 0; i < configs.size(); ++i) {
      attribs.config = configs[i];
      int _fd = static_cast<int>(
          syscall(__NR_perf_event_open, &attribs, 0, -1, group, 0UL));
      if (_fd == -1) {
        report_error("perf_event_open");
        return false;
      }
      all_fds.push_back(_fd);
      ioctl(_fd, PERF_EVENT_IOC_ID, &ids[i]);
      if (group == -1) {
        group = _fd;
        fd = _fd;
      }
    }
    // nr + time_enabled + time_running + 2*nr (value, id)
    temp_result_vec.assign(3 + 2 * num_events, 0);
    return true;
  }

  bool probe_scheduling() {
    if (fd == -1) return false;

    if (ioctl(fd, PERF_EVENT_IOC_RESET,  PERF_IOC_FLAG_GROUP) == -1) return false;
    if (ioctl(fd, PERF_EVENT_IOC_ENABLE, PERF_IOC_FLAG_GROUP) == -1) return false;

    volatile int sink = 0;
    for (int i = 0; i < 10000; ++i) sink += i;

    if (ioctl(fd, PERF_EVENT_IOC_DISABLE, PERF_IOC_FLAG_GROUP) == -1) return false;

    if (read(fd, temp_result_vec.data(), temp_result_vec.size() * 8) == -1) {
      return false;
    }
    uint64_t time_enabled = temp_result_vec[1];
    uint64_t time_running = temp_result_vec[2];
    return time_running > 0 && time_running == time_enabled;
  }

  void cleanup_fds() {
    for (int f : all_fds) close(f);
    all_fds.clear();
    fd = -1;
  }

  void report_error(const std::string &) { working = false; }
};

} // namespace counters

#endif // __linux__
#endif // COUNTERS_LINUX_PERF_EVENTS_H_
