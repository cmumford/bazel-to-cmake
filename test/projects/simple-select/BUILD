load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
    name = "message",
    srcs = ["main.cc", "message.h"] + select({
        "@bazel_tools//src/conditions:windows": ["message_win.cc"],
        "@bazel_tools//src/conditions:darwin": ["message_mac.cc"],
        "//conditions:default": ["message_default.cc"],
    })
)
