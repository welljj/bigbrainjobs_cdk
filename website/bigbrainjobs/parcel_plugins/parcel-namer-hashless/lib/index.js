"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;
var _plugin = require("@parcel/plugin");
var _path = _interopRequireDefault(require("path"));
function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }
var _default = new _plugin.Namer({
  name: function name(_ref) {
    var bundle = _ref.bundle;
    if (!bundle.needsStableName) {
      var filePath = bundle.getMainEntry().filePath;
      return _path["default"].basename(filePath);
    }

    // Allow the next namer to handle this bundle.
    return null;
  }
});
exports["default"] = _default;