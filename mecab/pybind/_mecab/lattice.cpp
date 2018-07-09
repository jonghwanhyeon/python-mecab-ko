#include <pybind11/pybind11.h>
#include <mecab.h>

namespace py = pybind11;

class Iterator {
private:
  const MeCab::Node *cursor;

public:
  Iterator(const MeCab::Node* cursor) : cursor(cursor) {}

  const MeCab::Node& operator*() const { return *cursor; }
  Iterator& operator++() { cursor = cursor->next; return *this; }
  bool operator==(const Iterator& rhs) const { return cursor == rhs.cursor;}
};

void initialize_lattice(py::module &m) {
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

  // Reference: https://taku910.github.io/mecab/doxygen/index.html
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
    .def("__iter__", [](MeCab::Lattice &self) {
      Iterator begin = Iterator(self.bos_node()->next); // beigin should point to the actual first element
      Iterator end = Iterator(self.eos_node());

      return py::make_iterator(begin, end);
    }, py::keep_alive<0, 1>()) // 0 -> iterator, 1 -> self
  ;
}