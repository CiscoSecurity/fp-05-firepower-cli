function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function _extends() { _extends = Object.assign ? Object.assign.bind() : function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }
/**
 * @fileOverview Polar Grid
 */
import React from 'react';
import { polarToCartesian } from '../util/PolarUtils';
import { filterProps } from '../util/ReactUtils';
var polarGridDefaultProps = {
  cx: 0,
  cy: 0,
  innerRadius: 0,
  outerRadius: 0,
  gridType: 'polygon',
  radialLines: true
};
var getPolygonPath = function getPolygonPath(radius, cx, cy, polarAngles) {
  var path = '';
  polarAngles.forEach(function (angle, i) {
    var point = polarToCartesian(cx, cy, radius, angle);
    if (i) {
      path += "L ".concat(point.x, ",").concat(point.y);
    } else {
      path += "M ".concat(point.x, ",").concat(point.y);
    }
  });
  path += 'Z';
  return path;
};

// Draw axis of radial line
var PolarAngles = function PolarAngles(props) {
  var cx = props.cx,
    cy = props.cy,
    innerRadius = props.innerRadius,
    outerRadius = props.outerRadius,
    polarAngles = props.polarAngles,
    radialLines = props.radialLines;
  if (!polarAngles || !polarAngles.length || !radialLines) {
    return null;
  }
  var polarAnglesProps = _objectSpread({
    stroke: '#ccc'
  }, filterProps(props));
  return /*#__PURE__*/React.createElement("g", {
    className: "recharts-polar-grid-angle"
  }, polarAngles.map(function (entry, i) {
    var start = polarToCartesian(cx, cy, innerRadius, entry);
    var end = polarToCartesian(cx, cy, outerRadius, entry);
    return /*#__PURE__*/React.createElement("line", _extends({}, polarAnglesProps, {
      key: "line-".concat(i) // eslint-disable-line react/no-array-index-key
      ,
      x1: start.x,
      y1: start.y,
      x2: end.x,
      y2: end.y
    }));
  }));
};

// Draw concentric circles
var ConcentricCircle = function ConcentricCircle(props) {
  var cx = props.cx,
    cy = props.cy,
    radius = props.radius,
    index = props.index;
  var concentricCircleProps = _objectSpread(_objectSpread({
    stroke: '#ccc'
  }, filterProps(props)), {}, {
    fill: 'none'
  });
  return /*#__PURE__*/React.createElement("circle", _extends({}, concentricCircleProps, {
    className: "recharts-polar-grid-concentric-circle",
    key: "circle-".concat(index),
    cx: cx,
    cy: cy,
    r: radius
  }));
};

// Draw concentric polygons
var ConcentricPolygon = function ConcentricPolygon(props) {
  var radius = props.radius,
    index = props.index;
  var concentricPolygonProps = _objectSpread(_objectSpread({
    stroke: '#ccc'
  }, filterProps(props)), {}, {
    fill: 'none'
  });
  return /*#__PURE__*/React.createElement("path", _extends({}, concentricPolygonProps, {
    className: "recharts-polar-grid-concentric-polygon",
    key: "path-".concat(index),
    d: getPolygonPath(radius, props.cx, props.cy, props.polarAngles)
  }));
};

// Draw concentric axis
// TODO Optimize the name
var ConcentricPath = function ConcentricPath(props) {
  var polarRadius = props.polarRadius,
    gridType = props.gridType;
  if (!polarRadius || !polarRadius.length) {
    return null;
  }
  return /*#__PURE__*/React.createElement("g", {
    className: "recharts-polar-grid-concentric"
  }, polarRadius.map(function (entry, i) {
    var key = i;
    if (gridType === 'circle') return /*#__PURE__*/React.createElement(ConcentricCircle, _extends({
      key: key
    }, props, {
      radius: entry,
      index: i
    }));
    return /*#__PURE__*/React.createElement(ConcentricPolygon, _extends({
      key: key
    }, props, {
      radius: entry,
      index: i
    }));
  }));
};
export var PolarGrid = function PolarGrid(props) {
  var outerRadius = props.outerRadius;
  if (outerRadius <= 0) {
    return null;
  }
  return /*#__PURE__*/React.createElement("g", {
    className: "recharts-polar-grid"
  }, /*#__PURE__*/React.createElement(PolarAngles, props), /*#__PURE__*/React.createElement(ConcentricPath, props));
};
PolarGrid.displayName = 'PolarGrid';
PolarGrid.defaultProps = polarGridDefaultProps;