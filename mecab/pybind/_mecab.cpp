#include <memory>
#include <pybind11/pybind11.h>
#include <mecab.h>

#include <iostream>

namespace py = pybind11;

// Reference: https://taku910.github.io/mecab/doxygen/index.html
PYBIND11_MODULE(_mecab, m) {
  // Parameters for MeCab::Node::stat
  m.attr("MECAB_NOR_NODE") = 0;
  m.attr("MECAB_UNK_NODE") = 1;
  m.attr("MECAB_BOS_NODE") = 2;
  m.attr("MECAB_EOS_NODE") = 3;
  m.attr("MECAB_EON_NODE") = 4;

  // Parameters for MeCab::DictionaryInfo::type
  m.attr("MECAB_SYS_DIC") = 0;
  m.attr("MECAB_USR_DIC") = 1;
  m.attr("MECAB_UNK_DIC") = 2;

  // Parameters for MeCab::Lattice::request_type
  m.attr("MECAB_ONE_BEST") = 1;
  m.attr("MECAB_NBEST") = 2;
  m.attr("MECAB_PARTIAL") = 4;
  m.attr("MECAB_MARGINAL_PROB") = 8;
  m.attr("MECAB_ALTERNATIVE") = 16;
  m.attr("MECAB_ALL_MORPHS") = 32;
  m.attr("MECAB_ALLOCATE_SENTENCE") = 64;

  // Parameters for MeCab::Lattice::boundary_constraint_type
  m.attr("MECAB_ANY_BOUNDARY") = 0;
  m.attr("MECAB_TOKEN_BOUNDARY") = 1;
  m.attr("MECAB_INSIDE_TOKEN") = 2;

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

  py::class_<MeCab::Path>(m, "Path")
    .def_readwrite("rnode", &MeCab::Path::rnode)
    .def_readwrite("rnext", &MeCab::Path::rnext)
    .def_readwrite("lnode", &MeCab::Path::lnode)
    .def_readwrite("lnext", &MeCab::Path::lnext)
    .def_readwrite("cost", &MeCab::Path::cost)
    .def_readwrite("prob", &MeCab::Path::prob)
  ;

  py::class_<MeCab::Lattice>(m, "Lattice")
    .def(py::init([]() {
      return std::unique_ptr<MeCab::Lattice>(MeCab::Lattice::create());
    }))
    .def("clear", [](MeCab::Lattice &self) {
      self.clear();
    })
    .def("is_available", [](MeCab::Lattice &self) {
      return self.is_available();
    })
    .def("bos_node", [](MeCab::Lattice &self) {
      return self.bos_node();
    }, py::return_value_policy::reference)
    .def("eos_node", [](MeCab::Lattice &self) {
      return self.eos_node();
    }, py::return_value_policy::reference)
    .def("end_nodes", [](MeCab::Lattice &self, size_t position) {
      return self.end_nodes(position);
    })
    .def("begin_nodes", [](MeCab::Lattice &self, size_t position) {
      return self.begin_nodes(position);
    }, py::return_value_policy::reference)
    .def("sentence", [](MeCab::Lattice &self) {
      return self.sentence();
    }, py::return_value_policy::reference)
    .def("set_sentence", [](MeCab::Lattice &self, const char *sentence) {
      self.set_sentence(sentence);
    })
    .def("set_sentence", [](MeCab::Lattice &self, const char *sentence, size_t length) {
      self.set_sentence(sentence, length);
    })
    .def("size", [](MeCab::Lattice &self) {
      return self.size();
    })
    .def("set_Z", [](MeCab::Lattice &self, double Z) {
      self.set_Z(Z);
    })
    .def("Z", [](MeCab::Lattice &self) {
      return self.Z();
    })
    .def("set_theta", [](MeCab::Lattice &self, float theta) {
      self.set_theta(theta);
    })
    .def("theta", [](MeCab::Lattice &self) {
      return self.theta();
    })
    .def("next", [](MeCab::Lattice &self) {
      return self.next();
    })
    .def("request_type", [](MeCab::Lattice &self) {
      return self.request_type();
    })
    .def("has_request_type", [](MeCab::Lattice &self, int request_type) {
      return self.has_request_type(request_type);
    })
    .def("set_request_type", [](MeCab::Lattice &self, int request_type) {
      self.set_request_type(request_type);
    })
    .def("add_request_type", [](MeCab::Lattice &self, int request_type) {
      self.add_request_type(request_type);
    })
    .def("remove_request_type", [](MeCab::Lattice &self, int request_type) {
      self.remove_request_type(request_type);
    })
    .def("new_node", [](MeCab::Lattice &self) {
      return self.newNode();
    }, py::return_value_policy::reference)
    .def("to_string", [](MeCab::Lattice &self) {
      return self.toString();
    })
    .def("to_string", [](MeCab::Lattice &self, const MeCab::Node *node) {
      return self.toString(node);
    })
    .def("enum_nbest_as_string", [](MeCab::Lattice &self, size_t n) {
      return self.enumNBestAsString(n);
    })
    .def("to_string", [](MeCab::Lattice &self, char *buffer, size_t size) {
      return self.toString(buffer, size);
    })
    .def("to_string", [](MeCab::Lattice &self, const MeCab::Node *node, char *buffer, size_t size) {
      return self.toString(node, buffer, size);
    })
    .def("enum_nbest_as_string", [](MeCab::Lattice &self, size_t n, char *buffer, size_t size) {
      return self.enumNBestAsString(n, buffer, size);
    })
    .def("has_constraint", [](MeCab::Lattice &self) {
      return self.has_constraint();
    })
    .def("boundary_constraint", [](MeCab::Lattice &self, size_t position) {
      return self.boundary_constraint(position);
    })
    .def("feature_constraint", [](MeCab::Lattice &self, size_t position) {
      return self.feature_constraint(position);
    })
    .def("set_boundary_constraint", [](MeCab::Lattice &self, size_t position, int boundary_constraint_type) {
      self.set_boundary_constraint(position, boundary_constraint_type);
    })
    .def("set_feature_constraint", [](MeCab::Lattice &self, size_t begin_position, size_t end_position, const char *feature) {
      self.set_feature_constraint(begin_position, end_position, feature);
    })
    .def("set_result", [](MeCab::Lattice &self, const char *result) {
      self.set_result(result);
    })
    .def("what", [](MeCab::Lattice &self) {
      return self.what();
    })
    .def("set_what", [](MeCab::Lattice &self, const char *text) {
      self.set_what(text);
    })
  ;

  py::class_<MeCab::DictionaryInfo>(m, "DictionaryInfo")
    .def_readonly("filename", &MeCab::DictionaryInfo::filename)
    .def_readonly("charset", &MeCab::DictionaryInfo::charset)
    .def_readwrite("size", &MeCab::DictionaryInfo::size)
    .def_readwrite("type", &MeCab::DictionaryInfo::type)
    .def_readwrite("lsize", &MeCab::DictionaryInfo::lsize)
    .def_readwrite("rsize", &MeCab::DictionaryInfo::rsize)
    .def_readwrite("version", &MeCab::DictionaryInfo::version)
    .def_readwrite("next", &MeCab::DictionaryInfo::next)
  ;

  py::class_<MeCab::Tagger>(m, "Tagger")
    .def(py::init([](const char *argument) {
      return std::unique_ptr<MeCab::Tagger>(MeCab::Tagger::create(argument));
    }))
    .def("parse", [](MeCab::Tagger &self, MeCab::Lattice *lattice) {
      return self.parse(lattice);
    })
    .def("parse", [](MeCab::Tagger &self, const char *text) {
      return self.parse(text);
    })
    .def("parse_to_node", [](MeCab::Tagger &self, const char *text) {
      return self.parseToNode(text);
    }, py::return_value_policy::reference)
    .def("set_theta", [](MeCab::Tagger &self, float theta) {
      self.set_theta(theta);
    })
    .def("theta", [](MeCab::Tagger &self) {
      return self.theta();
    })
    .def("dictionary_info", [](MeCab::Tagger &self) {
      return self.dictionary_info();
    }, py::return_value_policy::reference)
    .def("what", [](MeCab::Tagger &self) {
      return self.what();
    })
    .def("version", [](MeCab::Tagger &self) {
      return MeCab::Tagger::version();
    })
  ;
}