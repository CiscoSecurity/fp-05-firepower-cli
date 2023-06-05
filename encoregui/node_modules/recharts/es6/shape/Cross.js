function _extends() { _extends = Object.assign ? Object.assign.bind() : function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }
/**
 * @fileOverview Cross
 */
import React from 'react';
import classNames from 'classnames';
import { isNumber } from '../util/DataUtils';
import { filterProps } from '../util/ReactUtils';
var getPath = function getPath(x, y, width, height, top, left) {
  return "M".concat(x, ",").concat(top, "v").concat(height, "M").concat(left, ",").concat(y, "h").concat(width);
};
export var Cross = function Cross(props) {
  var x = props.x,
    y = props.y,
    width = props.width,
    height = props.height,
    top = props.top,
    left = props.left,
    className = props.className;
  if (!isNumber(x) || !isNumber(y) || !isNumber(width) || !isNumber(height) || !isNumber(top) || !isNumber(left)) {
    return null;
  }
  return /*#__PURE__*/React.createElement("path", _extends({}, filterProps(props, true), {
    className: classNames('recharts-cross', className),
    d: getPath(x, y, width, height, top, left)
  }));
};
Cross.defaultProps = {
  x: 0,
  y: 0,
  top: 0,
  left: 0,
  width: 0,
  height: 0
};