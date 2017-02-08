import os
from conans import ConanFile, ConfigureEnvironment
from conans.tools import download
from conans.tools import untargz
from conans.tools import cpu_count
from conans.tools import patch

class OpenFSTConan(ConanFile):
    name = "OpenFST"
    version = "1.4.1-kaldi"
    generators = "cmake"
    settings = { "os": ["Linux"],
                 "compiler": {"gcc": {"libcxx": ["libstdc++11"]},
                              "clang": {"libcxx": ["libstdc++11"]}},
                 "arch": ["x86_64"],
                 "build_type": ["Debug", "Release"]}
    license = "Apache 2.0"
    url = "http://openfst.org"
    source_url = "http://openfst.org/twiki/pub/FST/FstDownload/openfst-1.4.1.tar.gz"
    kaldi_patch_url = "https://raw.githubusercontent.com/kaldi-asr/kaldi/master/tools/extras/openfst-1.4.1.patch"
    kaldi_patch_path = "openfst-1.4.1.patch"
    unzipped_path = "openfst-1.4.1"

    def source(self):
        self.targz_name = os.path.basename(self.source_url)
        download(self.source_url, self.targz_name)
        untargz(self.targz_name)
        os.unlink(self.targz_name)

        # Apply Kaldi patch
        download(self.kaldi_patch_url, self.kaldi_patch_path)
        patch(self.unzipped_path, self.kaldi_patch_path, strip=1)

    def build(self):
        env = ConfigureEnvironment(self)
        configure_opts = "--prefix={} --enable-static --enable-shared --enable-far --enable-ngram-fsts LIBS=\"-ldl\"".format(self.package_folder)
        self.run("{} {}/{}/configure {}".format(env.command_line_env, self.conanfile_directory, self.unzipped_path, configure_opts))
        self.run("{} make -j{} install ".format(env.command_line_env, cpu_count()))

    def package(self):
        self.copy("*.h", dst="include/fst", src="include/fst")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.la", dst="lib", src="lib")
        self.copy("*.so*", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["fst"]
