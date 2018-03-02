import Foundation
import Swimsuit

for power in 20...30 {
  let size = 1 << power
  let sizeinmbytes = size * MemoryLayout<Int>.size / (1024 * 1024)
  print("trial \(size), data size in bytes \(sizeinmbytes) MB ")
  // could use an  IndexSet, but we want to illustrate a generic problem (not specific to Int)
  let d = Set<Int>(1...size)
  var dcopy = Set<Int>() // could make much faster by specify minimumCapacity
  let nanocopy = Swimsuit.nanotime {
     for i in d {
       dcopy.insert(i)
     }
  }
  print("time (s) : ", Double(nanocopy)/(1000*1000*1000))

}
