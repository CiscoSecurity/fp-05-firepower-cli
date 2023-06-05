"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Cross = void 0;
var _react = _interopRequireDefault(require("react"));
var _classnames = _interopRequireDefault(require("classnames"));
var _DataUtils = require("../util/DataUtils");
var _ReactUtils = require("../util/ReactUtils");
function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }
function _extends() { _extends = Object.assign ? Object.assign.bind() : function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); } /**
                                                                                                                                                                                                                                                                                                                                                     * @fileOverview Cross
                                                                                                                                                                                                                                                                                                                                                     */
var getPath = function getPath(x, y, width, height, top, left) {
  return "M".concat(x, ",").concat(top, "v").concat(height, "M").concat(left, ",").concat(y, "h").concat(width);
};
var Cross = function Cross(props) {
  var x = props.x,
    y = props.y,
    width = props.width,
    height = props.height,
    top = props.top,
    left = props.left,
    className = props.className;
  if (!(0, _DataUtils.isNumber)(x) || !(0, _DataUtils.isNumber)(y) || !(0, _DataUtils.isNumber)(width) || !(0, _DataUtils.isNumber)(height) || !(0, _DataUtils.isNumber)(top) || !(0, _DataUtils.isNumber)(left)) {
    return null;
  }
  return /*#__PURE__*/_react["default"].createElement("path", _extends({}, (0, _ReactUtils.filterProps)(props, true), {
    className: (0, _classnames["default"])('recharts-cross', className),
    d: getPath(x, y, width, height, top, left)
  }));
};
exports.Cross = Cross;
Cross.defaultProps = {
  x: 0,
  y: 0,
  top: 0,
  left: 0,
  width: 0,
  height: 0
};