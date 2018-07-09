#include <pybind11/pybind11.h>
#include <mecab.h>

namespace py = pybind11;

void initialize_node(py::module &m) {
  // Parameters for MeCab::Node::stat
  m.attr("MECAB_NOR_NODE") = 0;
  m.attr("MECAB_UNK_NODE") = 1;
  m.attr("MECAB_BOS_NODE") = 2;
  m.attr("MECAB_EOS_NODE") = 3;
  m.attr("MECAB_EON_NODE") = 4;

  // Reference: https://taku910.github.io/mecab/doxygen/index.html
  py::class_<MeCab::Node>(m, "Node")
    .def_readwrite("prev", &MeCab::Node::prev)
    .def_readwrite("next", &MeCab::Node::next)
    .def_readwrite("enext", &MeCab::Node::enext)
    .def_readwrite("bnext", &MeCab::Node::bnext)
    .def_readwrite("rpath", &MeCab::Node::rpath)
    .def_readwrite("lpath", &MeCab::Node::lpath)
    .def_property_readonly("surface", [](MeCab::Node &self) {
      return std::string(self.surface, self.length);
    })
    .def_readonly("feature", &MeCab::Node::feature)
    .def_readwrite("id", &MeCab::Node::id)
    .def_readwrite("length", &MeCab::Node::length)
    .def_readwrite("rlength", &MeCab::Node::rlength)
    .def_readwrite("rcAttr", &MeCab::Node::rcAttr)
    .def_readwrite("lcAttr", &MeCab::Node::lcAttr)
    .def_readwrite("posid", &MeCab::Node::posid)
    .def_readwrite("char_type", &MeCab::Node::char_type)
    .def_readwrite("stat", &MeCab::Node::stat)
    .def_readwrite("isbest", &MeCab::Node::isbest)
    .def_readwrite("alpha", &MeCab::Node::alpha)
    .def_readwrite("beta", &MeCab::Node::beta)
    .def_readwrite("prob", &MeCab::Node::prob)
    .def_readwrite("wcost", &MeCab::Node::wcost)
    .def_readwrite("cost", &MeCab::Node::cost)
  ;
}