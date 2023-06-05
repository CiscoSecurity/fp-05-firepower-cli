function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
import _isNil from "lodash/isNil";
import _isFunction from "lodash/isFunction";
import _uniqBy from "lodash/uniqBy";
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }
function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }
function _iterableToArrayLimit(arr, i) { var _i = null == arr ? null : "undefined" != typeof Symbol && arr[Symbol.iterator] || arr["@@iterator"]; if (null != _i) { var _s, _e, _x, _r, _arr = [], _n = !0, _d = !1; try { if (_x = (_i = _i.call(arr)).next, 0 === i) { if (Object(_i) !== _i) return; _n = !1; } else for (; !(_n = (_s = _x.call(_i)).done) && (_arr.push(_s.value), _arr.length !== i); _n = !0); } catch (err) { _d = !0, _e = err; } finally { try { if (!_n && null != _i["return"] && (_r = _i["return"](), Object(_r) !== _r)) return; } finally { if (_d) throw _e; } } return _arr; } }
function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }
/**
 * @fileOverview Tooltip
 */
import React, { useEffect, useState, useRef, useCallback } from 'react';
import { translateStyle } from 'react-smooth';
import classNames from 'classnames';
import { DefaultTooltipContent } from './DefaultTooltipContent';
import { Global } from '../util/Global';
import { isNumber } from '../util/DataUtils';
var CLS_PREFIX = 'recharts-tooltip-wrapper';
var EPS = 1;
function defaultUniqBy(entry) {
  return entry.dataKey;
}
function getUniqPayload(option, payload) {
  if (option === true) {
    return _uniqBy(payload, defaultUniqBy);
  }
  if (_isFunction(option)) {
    return _uniqBy(payload, option);
  }
  return payload;
}
function renderContent(content, props) {
  if ( /*#__PURE__*/React.isValidElement(content)) {
    return /*#__PURE__*/React.cloneElement(content, props);
  }
  if (_isFunction(content)) {
    return /*#__PURE__*/React.createElement(content, props);
  }
  return /*#__PURE__*/React.createElement(DefaultTooltipContent, props);
}
var tooltipDefaultProps = {
  active: false,
  allowEscapeViewBox: {
    x: false,
    y: false
  },
  reverseDirection: {
    x: false,
    y: false
  },
  offset: 10,
  viewBox: {
    x: 0,
    y: 0,
    height: 0,
    width: 0
  },
  coordinate: {
    x: 0,
    y: 0
  },
  // this doesn't exist on TooltipProps
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  cursorStyle: {},
  separator: ' : ',
  wrapperStyle: {},
  contentStyle: {},
  itemStyle: {},
  labelStyle: {},
  cursor: true,
  trigger: 'hover',
  isAnimationActive: !Global.isSsr,
  animationEasing: 'ease',
  animationDuration: 400,
  filterNull: true,
  useTranslate3d: false
};
export var Tooltip = function Tooltip(props) {
  var _classNames;
  var _useState = useState(-1),
    _useState2 = _slicedToArray(_useState, 2),
    boxWidth = _useState2[0],
    setBoxWidth = _useState2[1];
  var _useState3 = useState(-1),
    _useState4 = _slicedToArray(_useState3, 2),
    boxHeight = _useState4[0],
    setBoxHeight = _useState4[1];
  var _useState5 = useState(false),
    _useState6 = _slicedToArray(_useState5, 2),
    dismissed = _useState6[0],
    setDismissed = _useState6[1];
  var _useState7 = useState({
      x: 0,
      y: 0
    }),
    _useState8 = _slicedToArray(_useState7, 2),
    dismissedAtCoordinate = _useState8[0],
    setDismissedAtCoordinate = _useState8[1];
  var wrapperNode = useRef();
  var allowEscapeViewBox = props.allowEscapeViewBox,
    reverseDirection = props.reverseDirection,
    coordinate = props.coordinate,
    offset = props.offset,
    position = props.position,
    viewBox = props.viewBox;
  var handleKeyDown = useCallback(function (event) {
    if (event.key === 'Escape') {
      setDismissed(true);
      setDismissedAtCoordinate(function (prev) {
        return _objectSpread(_objectSpread({}, prev), {}, {
          x: coordinate === null || coordinate === void 0 ? void 0 : coordinate.x,
          y: coordinate === null || coordinate === void 0 ? void 0 : coordinate.y
        });
      });
    }
  }, [coordinate === null || coordinate === void 0 ? void 0 : coordinate.x, coordinate === null || coordinate === void 0 ? void 0 : coordinate.y]);
  useEffect(function () {
    var updateBBox = function updateBBox() {
      if (dismissed) {
        document.removeEventListener('keydown', handleKeyDown);
        if ((coordinate === null || coordinate === void 0 ? void 0 : coordinate.x) !== dismissedAtCoordinate.x || (coordinate === null || coordinate === void 0 ? void 0 : coordinate.y) !== dismissedAtCoordinate.y) {
          setDismissed(false);
        }
      } else {
        document.addEventListener('keydown', handleKeyDown);
      }
      if (wrapperNode.current && wrapperNode.current.getBoundingClientRect) {
        var box = wrapperNode.current.getBoundingClientRect();
        if (Math.abs(box.width - boxWidth) > EPS || Math.abs(box.height - boxHeight) > EPS) {
          setBoxWidth(box.width);
          setBoxHeight(box.height);
        }
      } else if (boxWidth !== -1 || boxHeight !== -1) {
        setBoxWidth(-1);
        setBoxHeight(-1);
      }
    };
    updateBBox();
    return function () {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [boxHeight, boxWidth, coordinate, dismissed, dismissedAtCoordinate.x, dismissedAtCoordinate.y, handleKeyDown]);
  var getTranslate = function getTranslate(_ref) {
    var key = _ref.key,
      tooltipDimension = _ref.tooltipDimension,
      viewBoxDimension = _ref.viewBoxDimension;
    if (position && isNumber(position[key])) {
      return position[key];
    }
    var negative = coordinate[key] - tooltipDimension - offset;
    var positive = coordinate[key] + offset;
    if (allowEscapeViewBox !== null && allowEscapeViewBox !== void 0 && allowEscapeViewBox[key]) {
      return reverseDirection[key] ? negative : positive;
    }
    if (reverseDirection !== null && reverseDirection !== void 0 && reverseDirection[key]) {
      var _tooltipBoundary = negative;
      var _viewBoxBoundary = viewBox[key];
      if (_tooltipBoundary < _viewBoxBoundary) {
        return Math.max(positive, viewBox[key]);
      }
      return Math.max(negative, viewBox[key]);
    }
    var tooltipBoundary = positive + tooltipDimension;
    var viewBoxBoundary = viewBox[key] + viewBoxDimension;
    if (tooltipBoundary > viewBoxBoundary) {
      return Math.max(negative, viewBox[key]);
    }
    return Math.max(positive, viewBox[key]);
  };
  var payload = props.payload,
    payloadUniqBy = props.payloadUniqBy,
    filterNull = props.filterNull,
    active = props.active,
    wrapperStyle = props.wrapperStyle,
    useTranslate3d = props.useTranslate3d,
    isAnimationActive = props.isAnimationActive,
    animationDuration = props.animationDuration,
    animationEasing = props.animationEasing;
  var finalPayload = getUniqPayload(payloadUniqBy, filterNull && payload && payload.length ? payload.filter(function (entry) {
    return !_isNil(entry.value);
  }) : payload);
  var hasPayload = finalPayload && finalPayload.length;
  var content = props.content;
  var outerStyle = _objectSpread({
    pointerEvents: 'none',
    visibility: !dismissed && active && hasPayload ? 'visible' : 'hidden',
    position: 'absolute',
    top: 0,
    left: 0
  }, wrapperStyle);
  var translateX, translateY;
  if (position && isNumber(position.x) && isNumber(position.y)) {
    translateX = position.x;
    translateY = position.y;
  } else if (boxWidth > 0 && boxHeight > 0 && coordinate) {
    translateX = getTranslate({
      key: 'x',
      tooltipDimension: boxWidth,
      viewBoxDimension: viewBox.width
    });
    translateY = getTranslate({
      key: 'y',
      tooltipDimension: boxHeight,
      viewBoxDimension: viewBox.height
    });
  } else {
    outerStyle.visibility = 'hidden';
  }
  outerStyle = _objectSpread(_objectSpread({}, translateStyle({
    transform: useTranslate3d ? "translate3d(".concat(translateX, "px, ").concat(translateY, "px, 0)") : "translate(".concat(translateX, "px, ").concat(translateY, "px)")
  })), outerStyle);
  if (isAnimationActive && active) {
    outerStyle = _objectSpread(_objectSpread({}, translateStyle({
      transition: "transform ".concat(animationDuration, "ms ").concat(animationEasing)
    })), outerStyle);
  }
  var cls = classNames(CLS_PREFIX, (_classNames = {}, _defineProperty(_classNames, "".concat(CLS_PREFIX, "-right"), isNumber(translateX) && coordinate && isNumber(coordinate.x) && translateX >= coordinate.x), _defineProperty(_classNames, "".concat(CLS_PREFIX, "-left"), isNumber(translateX) && coordinate && isNumber(coordinate.x) && translateX < coordinate.x), _defineProperty(_classNames, "".concat(CLS_PREFIX, "-bottom"), isNumber(translateY) && coordinate && isNumber(coordinate.y) && translateY >= coordinate.y), _defineProperty(_classNames, "".concat(CLS_PREFIX, "-top"), isNumber(translateY) && coordinate && isNumber(coordinate.y) && translateY < coordinate.y), _classNames));
  return (
    /*#__PURE__*/
    // ESLint is disabled to allow listening to the `Escape` key. Refer to
    // https://github.com/recharts/recharts/pull/2925
    // eslint-disable-next-line jsx-a11y/no-noninteractive-element-interactions
    React.createElement("div", {
      tabIndex: -1,
      role: "dialog",
      className: cls,
      style: outerStyle,
      ref: wrapperNode
    }, renderContent(content, _objectSpread(_objectSpread({}, props), {}, {
      payload: finalPayload
    })))
  );
};

// needs to be set so that renderByOrder can find the correct handler function
Tooltip.displayName = 'Tooltip';

/**
 * needs to be set so that renderByOrder can access an have default values for
 * children.props when there are no props set by the consumer
 * doesn't work if using default parameters
 */
Tooltip.defaultProps = tooltipDefaultProps;