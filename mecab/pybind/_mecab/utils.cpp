#include "utils.h"

std::string escape(const std::string &text) {
  std::regex pattern("([\"\\\\])");
  return std::regex_replace(text, pattern, "\\$1");
}