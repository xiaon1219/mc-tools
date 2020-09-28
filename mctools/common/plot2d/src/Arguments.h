#include <iostream>
#include <limits>
#include <sys/ioctl.h>

#include <boost/program_options.hpp>
#include <boost/algorithm/string/replace.hpp>

namespace po=boost::program_options;

class Plane {
private:
  std::string value;
public:
  Plane(std::string const &val):
    value(val)
  {
  }

  operator std::string() const
  {
    return value;
  }

  friend std::ostream& operator<<(std::ostream& os, const Plane& p)
  {
    os << p.value;
    return os;
  }
};

class Arguments {
 private:
  int argc;
  const char **argv;
  po::variables_map vm;
 public:
  Arguments(int ac, const char **av);
  po::variables_map GetMap() const { return &vm; }
  bool test() const;
};
