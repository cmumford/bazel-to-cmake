NUM_CPUS=10
CMAKE_BUILD_DIR=build_cmake
CMAKE_BUILD_FILE=CMakeLists.txt
CMAKE_ARGS=""
BAZEL_TO_CMAKE=~/src/bazel-to-cmake/bazel_to_cmake.py

.PHONY: default
default: build

.PHONY: clean
clean:
	rm -rf $(CMAKE_BUILD_DIR)
	bazel clean

.PHONY: build-bazel
build-bazel:
	bazel build :dosum

$(CMAKE_BUILD_DIR):
	mkdir $(CMAKE_BUILD_DIR)

.PHONY: build-cmake
build-cmake: $(CMAKE_BUILD_DIR)
	cd $(CMAKE_BUILD_DIR) && cmake $(MAKE_ARGS) .. && cmake --build . --parallel=$(NUM_CPUS)

.PHONY: build
build: build-cmake build-bazel
