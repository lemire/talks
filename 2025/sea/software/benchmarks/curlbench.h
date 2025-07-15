#include <curl/curl.h>
#include <string>
#include <stdexcept>

size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    size_t total_size = size * nmemb;
    userp->append(static_cast<char*>(contents), total_size);
    return total_size;
}

std::string load_rss_feed() {
    CURL* curl = curl_easy_init();
    if (!curl) {
        throw std::runtime_error("Échec de l'initialisation de curl");
    }

    std::string url = "https://lemire.me/blog/feed/";
    std::string result;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &result);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        curl_easy_cleanup(curl);
        throw std::runtime_error("Échec du chargement : " + std::string(curl_easy_strerror(res)));
    }

    curl_easy_cleanup(curl);
    return result;
}