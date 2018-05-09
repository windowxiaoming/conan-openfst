import os
from conans import ConanFile, CMake, tools, RunEnvironment

class OpenFSTTestConan(ConanFile):
    user = os.getenv("CONAN_USERNAME", "laeknaromur")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "OpenFST/1.6.5@{}/{}".format(user, channel)
    build_requires = "cmake_installer/3.10.0@conan/stable"
    settings = "os", "compiler", "arch", "build_type"
    generators = "virtualenv", "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        env = RunEnvironment(self)
        with tools.environment_append(env.vars):
            self.run(os.path.join("bin", "fst_test"))
