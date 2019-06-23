# hasher
A command tool for easily calculate file or dictionary hash value.
## Usage
```
Usage: hasher [path][-m [hash method]][-h][-q]
   -h    Show help
   -q    Quiet mode, no output.
   -m [hash method]      Must be in [md5, sha1, sha256, sha512, blake2b, blake2s]
```
## Demo
![](https://github.com/REFunction/hasher/blob/master/demo.png)
## Buffer Size
You can ignore this part without impacting on your use.

hasher uses 256KB(2^18) bytes as the size of reading buffer. This comes from the following experiment.
![](https://github.com/REFunction/hasher/blob/master/speed-test.png)
