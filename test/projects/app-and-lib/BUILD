load("@rules_cc//cc:defs.bzl", "cc_binary", "cc_library")

cc_library(
    name = "sum",
    srcs = ["sum.cc"],
    hdrs = ["sum.h"],
)

cc_binary(
    name = "dosum",
    srcs = ["main.cc"],
    deps = [":sum"],
)
