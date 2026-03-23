var SearchPrompt = (function (React) {
    'use strict';

    /******************************************************************************
    Copyright (c) Microsoft Corporation.

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
    REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
    INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
    OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
    PERFORMANCE OF THIS SOFTWARE.
    ***************************************************************************** */
    /* global Reflect, Promise, SuppressedError, Symbol */


    var __assign = function() {
        __assign = Object.assign || function __assign(t) {
            for (var s, i = 1, n = arguments.length; i < n; i++) {
                s = arguments[i];
                for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
            }
            return t;
        };
        return __assign.apply(this, arguments);
    };

    function __awaiter(thisArg, _arguments, P, generator) {
        function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
        return new (P || (P = Promise))(function (resolve, reject) {
            function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
            function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
            function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    }

    function __generator(thisArg, body) {
        var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
        return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
        function verb(n) { return function (v) { return step([n, v]); }; }
        function step(op) {
            if (f) throw new TypeError("Generator is already executing.");
            while (g && (g = 0, op[0] && (_ = 0)), _) try {
                if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
                if (y = 0, t) op = [op[0] & 2, t.value];
                switch (op[0]) {
                    case 0: case 1: t = op; break;
                    case 4: _.label++; return { value: op[1], done: false };
                    case 5: _.label++; y = op[1]; op = [0]; continue;
                    case 7: op = _.ops.pop(); _.trys.pop(); continue;
                    default:
                        if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                        if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                        if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                        if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                        if (t[2]) _.ops.pop();
                        _.trys.pop(); continue;
                }
                op = body.call(thisArg, _);
            } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
            if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
        }
    }

    function __read(o, n) {
        var m = typeof Symbol === "function" && o[Symbol.iterator];
        if (!m) return o;
        var i = m.call(o), r, ar = [], e;
        try {
            while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
        }
        catch (error) { e = { error: error }; }
        finally {
            try {
                if (r && !r.done && (m = i["return"])) m.call(i);
            }
            finally { if (e) throw e.error; }
        }
        return ar;
    }

    function __spreadArray(to, from, pack) {
        if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
            if (ar || !(i in from)) {
                if (!ar) ar = Array.prototype.slice.call(from, 0, i);
                ar[i] = from[i];
            }
        }
        return to.concat(ar || Array.prototype.slice.call(from));
    }

    typeof SuppressedError === "function" ? SuppressedError : function (error, suppressed, message) {
        var e = new Error(message);
        return e.name = "SuppressedError", e.error = error, e.suppressed = suppressed, e;
    };

    function _typeof(o) {
      "@babel/helpers - typeof";

      return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) {
        return typeof o;
      } : function (o) {
        return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o;
      }, _typeof(o);
    }

    var serverURL = '/api/search';
    var defaults = {
      error: 'An error has occured, please reload the page or try again later.',
      minSearchString: 3,
      group: 'All',
      groupCourses: 'Courses',
      pageSize: 10,
      authorizedKeys: ['filters', 'group', 'scholarshipgroup', 'page', 'pageid', 'pagesize', 'sorttype', 'sortvalue', 'term'],
      sortOptions: {
        name: '',
        label: 'Select sort option',
        prefix: 'Sort by:',
        optionsLabel: 'sort by options list'
      },
      clearFlag: {
        filter: 'All',
        status: false
      }
    };
    var END_POINTS = {
      search: "".concat(serverURL, "/contentsearch"),
      autocomplete: "".concat(serverURL, "/quicksearch"),
      courses: "".concat(serverURL, "/coursesearch"),
      scholarships: "".concat(serverURL, "/scholarshipsearch")
    };
    var filtersJoint = '@@@@@@';
    /**
     * This fetches data to an endpoint
     * @param endpoint string
     * @param body string - payload
     * @returns object
     */
    var dataFetcher = function dataFetcher(endpoint, body) {
      return __awaiter(void 0, void 0, void 0, function () {
        var response, data;
        return __generator(this, function (_a) {
          switch (_a.label) {
            case 0:
              _a.trys.push([0, 3,, 4]);
              response = fetch(endpoint, {
                method: 'POST',
                headers: {
                  'Content-type': 'application/json'
                },
                body: JSON.stringify(body)
              });
              return [4 /*yield*/, response];
            case 1:
              if (!_a.sent().ok) {
                throw new Error('Network response was not Ok');
              }
              return [4 /*yield*/, response];
            case 2:
              data = _a.sent().json();
              return [2 /*return*/, data];
            case 3:
              _a.sent();
              return [3 /*break*/, 4];
            case 4:
              return [2 /*return*/];
          }
        });
      });
    };
    var useDebounce = function useDebounce(inputValue, delay) {
      var _a = __read(React.useState(inputValue), 2),
        debouncedValue = _a[0],
        setDebouncedValue = _a[1];
      React.useEffect(function () {
        var handler = setTimeout(function () {
          setDebouncedValue(inputValue);
        }, delay);
        return function () {
          clearTimeout(handler);
        };
      }, [inputValue, delay]);
      return debouncedValue;
    };
    var getType = function getType(obj) {
      var lowerCaseTheFirstLetter = function lowerCaseTheFirstLetter(str) {
        return str[0].toLowerCase() + str.slice(1);
      };
      var type = _typeof(obj);
      if (type !== 'object') {
        return type;
      }
      return lowerCaseTheFirstLetter(Object.prototype.toString.call(obj).replace(/^\[object (\S+)\]$/, '$1'));
    };
    var validateAutoCompleteData = function validateAutoCompleteData(data) {
      var defaultResponse = {
        results: true,
        suggestions: true,
        log: []
      };
      var updatedResponse = __assign({}, defaultResponse);
      if (data) {
        var results = data.results,
          suggestions = data.suggestions;
        if (getType(results) === 'array' && getType(suggestions) === 'array') {
          // Checking data integrity for: Results
          if (results.length > 0) {
            var tempInvalidResults_2 = [];
            results.map(function (result) {
              if (!result.contentType || !result.title || !result.url) {
                updatedResponse.results = false;
                tempInvalidResults_2.push(!result.contentType ? 'contentType' : '', !result.title ? 'title' : '', !result.url ? 'url' : '');
              }
            });
            if (tempInvalidResults_2.length > 0) {
              updatedResponse.log.push({
                'Results data missing': __spreadArray([], __read(new Set(tempInvalidResults_2)), false).filter(function (entry) {
                  return entry !== '';
                })
              });
            }
          }
          // Checking data integrity for: Suggestions
          if (suggestions.length > 0) {
            var tempInvalidSuggestions_1 = [];
            suggestions.map(function (suggestion) {
              if (typeof suggestion !== 'string') {
                updatedResponse.suggestions = false;
                tempInvalidSuggestions_1.push('not a string');
              }
            });
            if (tempInvalidSuggestions_1.length > 0) {
              updatedResponse.log.push({
                'Suggestions data invalid': __spreadArray([], __read(new Set(tempInvalidSuggestions_1)), false).filter(function (entry) {
                  return entry !== '';
                })
              });
            }
          }
        } else {
          return {
            results: false,
            suggestions: false,
            log: ['Minimum data structure not met.']
          };
        }
      }
      return updatedResponse;
    };

    function getDefaultExportFromCjs (x) {
    	return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, 'default') ? x['default'] : x;
    }

    var classnames = {exports: {}};

    (function (module) {
      /* global define */

      (function () {

        var hasOwn = {}.hasOwnProperty;
        function classNames() {
          var classes = '';
          for (var i = 0; i < arguments.length; i++) {
            var arg = arguments[i];
            if (arg) {
              classes = appendClass(classes, parseValue(arg));
            }
          }
          return classes;
        }
        function parseValue(arg) {
          if (typeof arg === 'string' || typeof arg === 'number') {
            return arg;
          }
          if (_typeof(arg) !== 'object') {
            return '';
          }
          if (Array.isArray(arg)) {
            return classNames.apply(null, arg);
          }
          if (arg.toString !== Object.prototype.toString && !arg.toString.toString().includes('[native code]')) {
            return arg.toString();
          }
          var classes = '';
          for (var key in arg) {
            if (hasOwn.call(arg, key) && arg[key]) {
              classes = appendClass(classes, key);
            }
          }
          return classes;
        }
        function appendClass(value, newClass) {
          if (!newClass) {
            return value;
          }
          if (value) {
            return value + ' ' + newClass;
          }
          return value + newClass;
        }
        if (module.exports) {
          classNames["default"] = classNames;
          module.exports = classNames;
        } else {
          window.classNames = classNames;
        }
      })();
    })(classnames);
    var classnamesExports = classnames.exports;
    var classNames = /*@__PURE__*/getDefaultExportFromCjs(classnamesExports);

    var ContentTypeFilter = function ContentTypeFilter(props) {
      var introText = 'Category Filters:';
      var groupFacets = props.groupFacets,
        _a = props.callBack,
        callBack = _a === void 0 ? function () {} : _a,
        _b = props.allowUnselect,
        allowUnselect = _b === void 0 ? false : _b,
        _c = props.isHeader,
        isHeader = _c === void 0 ? false : _c,
        preSelected = props.preSelected,
        _d = props.showCounts,
        showCounts = _d === void 0 ? true : _d;
      var _e = __read(React.useState(preSelected), 2),
        selectedValue = _e[0],
        setSelectedValue = _e[1];
      /**
       * This toggles the contentType buttons (search prompt) or sends the selected value (search results)
       * @param value string
       */
      var handleSelect = function handleSelect(value) {
        if (value === selectedValue && allowUnselect) {
          callBack(defaults.group);
          setSelectedValue(defaults.group);
        } else {
          setSelectedValue(value);
          callBack(value);
        }
      };
      /**
       * Updates the selected value on change
       */
      React.useEffect(function () {
        setSelectedValue(preSelected);
      }, [preSelected]);
      return /*#__PURE__*/React.createElement("div", {
        className: classNames("contentTypeFilter", {
          'contentTypeFilter--header': isHeader
        })
      }, /*#__PURE__*/React.createElement("div", {
        role: 'group',
        "aria-labelledby": 'categoryFiltersLabel',
        className: 'contentTypeFilter__group'
      }, /*#__PURE__*/React.createElement("span", {
        id: 'categoryFiltersLabel',
        className: 'sr-only'
      }, introText), groupFacets === null || groupFacets === void 0 ? void 0 : groupFacets.map(function (groupFacet) {
        var value = groupFacet.value,
          _a = groupFacet.count,
          count = _a === void 0 ? 0 : _a,
          name = groupFacet.name;
        return /*#__PURE__*/React.createElement("button", {
          key: groupFacet.value,
          className: classNames('contentTypeFilter__button', {
            'contentTypeFilter__button--selected': value === selectedValue
          }),
          disabled: !isHeader && count === 0,
          role: 'radio',
          "aria-checked": value === selectedValue,
          "aria-label": count > 0 ? "".concat(name, " item count ").concat(count) : undefined,
          onClick: function onClick() {
            return handleSelect(value);
          }
        }, name, ' ', showCounts && count > 0 && ( /*#__PURE__*/React.createElement("span", {
          className: ''
        }, "(", count.toLocaleString(), ")")));
      })));
    };

    var CurrentQuickLinks = function CurrentQuickLinks(props) {
      var links = props.links,
        label = props.label;
      return /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__quick-links'
      }, /*#__PURE__*/React.createElement("h2", {
        className: 'searchPrompt__quick-links-label'
      }, label), /*#__PURE__*/React.createElement("ul", {
        className: 'searchPrompt__quick-links-list'
      }, links.map(function (link) {
        return /*#__PURE__*/React.createElement("li", {
          key: link.text,
          className: ''
        }, /*#__PURE__*/React.createElement("a", {
          href: link.href,
          target: link.target,
          className: 'searchPrompt__link'
        }, /*#__PURE__*/React.createElement("div", {
          className: 'searchPrompt__link-item'
        }, /*#__PURE__*/React.createElement("i", {
          className: 'searchPrompt__link-icon',
          "aria-hidden": 'true'
        }, "arrow_right_alt"), /*#__PURE__*/React.createElement("span", {
          className: 'searchPrompt__link-text'
        }, link.text))));
      })));
    };

    var getAutoCompletes = function getAutoCompletes(props) {
      return __awaiter(void 0, void 0, void 0, function () {
        var _a, baseURL, searchTerm, contentType, callBack, pageId, body, response, validData, aggregatedAutocompleteItems;
        var _b, _c;
        return __generator(this, function (_d) {
          switch (_d.label) {
            case 0:
              _a = props.baseURL, baseURL = _a === void 0 ? '' : _a, searchTerm = props.searchTerm, contentType = props.contentType, callBack = props.callBack, pageId = props.pageId;
              if (!(searchTerm.length >= defaults.minSearchString)) return [3 /*break*/, 2];
              body = {
                Term: searchTerm,
                Group: contentType || defaults.group,
                Filters: []
              };
              if (pageId) {
                body.PageId = pageId;
              }
              return [4 /*yield*/, dataFetcher("".concat(baseURL).concat(END_POINTS.autocomplete), body)];
            case 1:
              response = _d.sent();
              if (response === null || response === void 0 ? void 0 : response.results) {
                validData = validateAutoCompleteData(response);
                aggregatedAutocompleteItems = {
                  items: [],
                  suggestions: []
                };
                if (validData.results) {
                  (_b = aggregatedAutocompleteItems.items) === null || _b === void 0 ? void 0 : _b.push.apply(_b, __spreadArray([], __read(response.results), false));
                }
                if (validData.suggestions) {
                  (_c = aggregatedAutocompleteItems.suggestions) === null || _c === void 0 ? void 0 : _c.push.apply(_c, __spreadArray([], __read(response.suggestions), false));
                }
                if (aggregatedAutocompleteItems.items.length > 0 || aggregatedAutocompleteItems.suggestions.length > 0) {
                  callBack(aggregatedAutocompleteItems);
                } else {
                  callBack([]);
                }
              }
              return [3 /*break*/, 3];
            case 2:
              callBack(undefined);
              _d.label = 3;
            case 3:
              return [2 /*return*/];
          }
        });
      });
    };
    /**
     * This breaks up the text to insert a <span /> surrounding the martched "search term"
     * @param props Object
     * @returns JSX
     */
    var AutoComplete = function AutoComplete(props) {
      var searchTerm = props.searchTerm,
        item = props.item;
      var regex = new RegExp(searchTerm, 'ig');
      var split = item.split(regex);
      var matches = item.match(regex) || [];
      var result = [];
      for (var i = 0; i <= split.length; i += 1) {
        result.push(split[i]);
        if (matches[i]) {
          result.push( /*#__PURE__*/React.createElement("span", {
            key: i,
            className: 'autocompletes__match'
          }, matches[i]));
        }
      }
      return /*#__PURE__*/React.createElement("span", null, result);
    };
    var AutoCompletes = function AutoCompletes(props) {
      var searchTerm = props.searchTerm,
        items = props.items,
        suggestions = props.suggestions,
        suggestionsCallBack = props.suggestionsCallBack,
        useAsSearch = props.useAsSearch,
        itemsCallBack = props.itemsCallBack;
      return /*#__PURE__*/React.createElement("div", {
        className: 'autocompletes__list-wrapper'
      }, /*#__PURE__*/React.createElement("ul", {
        id: 'suggestions-list',
        role: 'listbox',
        "aria-labelledby": 'global-search',
        className: 'autocompletes__list',
        tabIndex: 2
      }, items.slice(0, 3).map(function (item, index) {
        return /*#__PURE__*/React.createElement("li", {
          role: 'option',
          className: 'autocompletes__item',
          key: "".concat(index, "-").concat(item.title)
        }, useAsSearch && itemsCallBack ? ( /*#__PURE__*/React.createElement("a", {
          href: '#',
          onClick: function onClick(e) {
            e.preventDefault();
            itemsCallBack(item.title);
          },
          className: 'autocompletes__link link'
        }, /*#__PURE__*/React.createElement(AutoComplete, {
          searchTerm: searchTerm,
          item: item.title
        }), item.contentType && ( /*#__PURE__*/React.createElement("span", {
          className: 'autocompletes__type'
        }, item.contentType)))) : ( /*#__PURE__*/React.createElement("a", {
          href: item.url,
          className: 'autocompletes__link link'
        }, /*#__PURE__*/React.createElement(AutoComplete, {
          searchTerm: searchTerm,
          item: item.title
        }), item.contentType && ( /*#__PURE__*/React.createElement("span", {
          className: 'autocompletes__type'
        }, item.contentType)))));
      }), suggestions.map(function (suggestion, index) {
        return /*#__PURE__*/React.createElement("li", {
          role: 'option',
          className: 'autocompletes__item',
          key: "".concat(index, "-suggestion-").concat(suggestion)
        }, /*#__PURE__*/React.createElement("a", {
          href: '#',
          onClick: function onClick(e) {
            e.preventDefault();
            suggestionsCallBack(suggestion);
          },
          className: 'autocompletes__link link'
        }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement(AutoComplete, {
          searchTerm: searchTerm,
          item: suggestion
        }), "...")));
      })));
    };

    var SubFilters = function SubFilters(props) {
      var currentGroupFacetName = props.currentGroupFacetName,
        filtersCount = props.filtersCount,
        filtersDropdownOpen = props.filtersDropdownOpen,
        tempFilters = props.tempFilters,
        callBack = props.callBack;
      return /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__filter-dropdown-wrapper'
      }, /*#__PURE__*/React.createElement("button", {
        tabIndex: 0,
        className: classNames("searchPrompt__filter-dropdown-button", {
          'searchPrompt__filter-dropdown-button--open': filtersDropdownOpen
        }),
        onClick: callBack.dropdown
      }, /*#__PURE__*/React.createElement("span", {
        className: 'searchPrompt__filter-dropdown-button-content'
      }, currentGroupFacetName, filtersCount ? ( /*#__PURE__*/React.createElement("span", {
        className: 'searchPrompt__filters-count'
      }, filtersCount)) : null), /*#__PURE__*/React.createElement("i", {
        className: 'icon__lg searchPrompt__filter-dropdown-icon',
        "aria-hidden": 'true'
      }, "keyboard_arrow_down")), /*#__PURE__*/React.createElement("div", {
        "aria-hidden": !filtersDropdownOpen,
        className: classNames("searchPrompt__filter-dropdown", {
          'searchPrompt__filter-dropdown--show': filtersDropdownOpen
        })
      }, /*#__PURE__*/React.createElement("ul", {
        className: 'searchPrompt__filter-dropdown-list'
      }, tempFilters === null || tempFilters === void 0 ? void 0 : tempFilters.options.map(function (option) {
        return /*#__PURE__*/React.createElement("li", {
          key: option.value,
          className: 'searchPrompt__filter-dropdown-list-item'
        }, /*#__PURE__*/React.createElement("button", {
          className: 'group searchPrompt__filter-select-button',
          onClick: function onClick() {
            return callBack.select(option);
          },
          "aria-checked": option.selected
        }, /*#__PURE__*/React.createElement("span", {
          className: 'searchPrompt__filter-label'
        }, option.name), /*#__PURE__*/React.createElement("span", {
          className: classNames("searchPrompt__filter-selected", {
            'searchPrompt__filter-selected--active': option.selected
          })
        }, /*#__PURE__*/React.createElement("i", {
          className: 'icon__md',
          "aria-hidden": 'true'
        }, "check"))));
      })), /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__button-wrapper'
      }, /*#__PURE__*/React.createElement("button", {
        className: 'button link__color--primary button__type--secondary button__size--base searchPrompt__clear-filter-button',
        onClick: callBack.clear
      }, "Clear All"), /*#__PURE__*/React.createElement("button", {
        className: 'button button__color--primary button__type--primary button__size--base searchPrompt__apply-filter-button',
        onClick: callBack.apply
      }, "Apply"))));
    };

    var SearchPrompt = function SearchPrompt(props) {
      var _a = props.baseURL,
        baseURL = _a === void 0 ? '' : _a,
        resultsURL = props.resultsURL,
        introText = props.introText,
        placeholders = props.placeholders,
        promptContentTypes = props.promptContentTypes;
      var _b = __read(React.useState(null), 2),
        currentContentType = _b[0],
        setContentType = _b[1];
      var _c = __read(React.useState(false), 2),
        filtersDropdownOpen = _c[0],
        setfiltersDropdown = _c[1];
      var _d = __read(React.useState(''), 2),
        searchInput = _d[0],
        setSearchInput = _d[1];
      var _e = __read(React.useState(), 2),
        autoCompletes = _e[0],
        setAutoCompletes = _e[1];
      var _f = __read(React.useState(null), 2),
        filters = _f[0],
        setFilters = _f[1];
      var _g = __read(React.useState(placeholders["default"]), 2),
        placeholder = _g[0],
        setPlaceholder = _g[1];
      var _h = __read(React.useState(null), 2),
        tempFilters = _h[0],
        setTempFilters = _h[1];
      var debouncedSearchTerm = useDebounce(searchInput, 700);
      /**
       * This reads the current filters selected and returns an array of their values.
       * To be used in data sent to the back-end.
       * @returns string[]
       */
      var getSelectedFilters = function getSelectedFilters() {
        var appliedFilters = filters === null || filters === void 0 ? void 0 : filters.options.filter(function (option) {
          return option.selected;
        });
        var filtersList = [];
        appliedFilters === null || appliedFilters === void 0 ? void 0 : appliedFilters.map(function (filter) {
          filtersList.push(filter.value);
        });
        return filtersList;
      };
      var toggleDropdown = function toggleDropdown() {
        setfiltersDropdown(!filtersDropdownOpen);
      };
      var filtersCount = React.useMemo(function () {
        return filters === null || filters === void 0 ? void 0 : filters.options.filter(function (option) {
          return option.selected;
        }).length;
      }, [filters]);
      var currentQuickLinks = React.useMemo(function () {
        var _a;
        return ((_a = promptContentTypes.find(function (item) {
          return item.value === currentContentType;
        })) === null || _a === void 0 ? void 0 : _a.quicklinks) || null;
      }, [currentContentType]);
      var clearInput = function clearInput() {
        setSearchInput('');
      };
      var currentGroupFacet = React.useMemo(function () {
        var _a;
        return (_a = promptContentTypes.find(function (item) {
          return item.value === currentContentType;
        })) === null || _a === void 0 ? void 0 : _a.filters;
      }, [currentContentType]);
      var clearFilters = function clearFilters() {
        if (filters) {
          setFilters(__assign(__assign({}, filters), {
            options: filters === null || filters === void 0 ? void 0 : filters.options.map(function (option) {
              return __assign(__assign({}, option), {
                selected: false
              });
            })
          }));
          setfiltersDropdown(false);
        }
      };
      var applyFilters = function applyFilters() {
        setFilters(tempFilters);
        setfiltersDropdown(false);
      };
      var selectFilterOption = function selectFilterOption(_a) {
        var value = _a.value;
        if (tempFilters) {
          var updatedFilters = __assign({}, tempFilters);
          var updatedOptions = updatedFilters === null || updatedFilters === void 0 ? void 0 : updatedFilters.options.map(function (option) {
            if (option.value === value) {
              return __assign(__assign({}, option), {
                selected: !option.selected
              });
            }
            return option;
          });
          updatedFilters.options = updatedOptions;
          setTempFilters(updatedFilters);
        }
      };
      var handleContentTypeChange = function handleContentTypeChange(value) {
        setContentType(value);
        setfiltersDropdown(false);
      };
      var sendToResultsPage = function sendToResultsPage() {
        if (searchInput.length > 0) {
          var body = {
            term: searchInput,
            group: currentContentType || defaults.group,
            filters: getSelectedFilters().join(filtersJoint)
          };
          var bodyToParams = new URLSearchParams(body).toString();
          location.href = "".concat(resultsURL, "?").concat(bodyToParams);
        }
      };
      /**
       * This listens to key strokes in the search input, and if there is a search term, and the enter key is hit, it submits the search
       * @param key string
       */
      var supportEnterKey = function supportEnterKey(key) {
        if (searchInput.length > 0 && key === 'Enter') {
          sendToResultsPage();
        }
      };
      React.useEffect(function () {
        if (debouncedSearchTerm) {
          // Query API and populate the auto completes array
          getAutoCompletes({
            baseURL: baseURL,
            searchTerm: debouncedSearchTerm,
            contentType: currentContentType,
            callBack: setAutoCompletes
          });
        }
      }, [debouncedSearchTerm]);
      React.useEffect(function () {
        var _a;
        setFilters(((_a = promptContentTypes.find(function (item) {
          return item.value === currentContentType;
        })) === null || _a === void 0 ? void 0 : _a.filters) || null);
        setPlaceholder(placeholders[(currentContentType || '').toLowerCase()] || placeholders["default"]);
      }, [currentContentType]);
      React.useEffect(function () {
        // Clear the auto-complete array
        setAutoCompletes(undefined);
      }, [searchInput, currentContentType]);
      React.useEffect(function () {
        if (filtersDropdownOpen) setTempFilters(filters);
      }, [filtersDropdownOpen]);
      return /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt'
      }, /*#__PURE__*/React.createElement("div", {
        className: "searchPrompt__inner"
      }, /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__heading-wrapper'
      }, /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__heading'
      }, introText), /*#__PURE__*/React.createElement(ContentTypeFilter, {
        groupFacets: promptContentTypes,
        callBack: function callBack(value) {
          return handleContentTypeChange(value);
        },
        allowUnselect: true,
        isHeader: true
      })), /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__form-wrapper'
      }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
        className: 'searchPrompt__search-input-wrapper'
      }, /*#__PURE__*/React.createElement("label", {
        htmlFor: 'global-search',
        className: 'sr-only',
        id: 'global-search-label'
      }, "Search:"), /*#__PURE__*/React.createElement("input", {
        type: 'text',
        id: 'global-search',
        "aria-controls": 'suggestions-list',
        "aria-labelledby": 'global-search-label',
        className: 'searchPrompt__search-input',
        placeholder: placeholder,
        value: searchInput,
        onChange: function onChange(e) {
          setSearchInput(e.target.value);
        },
        onKeyUp: function onKeyUp(e) {
          return supportEnterKey(e.key);
        },
        autoComplete: 'off'
      }), (searchInput === null || searchInput === void 0 ? void 0 : searchInput.length) ? ( /*#__PURE__*/React.createElement("button", {
        className: 'button button__color--tertiary button__type--secondary button__size--base button__icon searchPrompt__input-clear-button',
        "aria-label": 'clear input',
        onClick: clearInput,
        tabIndex: 0
      }, /*#__PURE__*/React.createElement("i", {
        className: 'searchPrompt__clear-icon',
        "aria-hidden": 'true'
      }, "close"))) : null, currentGroupFacet && typeof filtersCount === 'number' && ( /*#__PURE__*/React.createElement(SubFilters, {
        filtersCount: filtersCount,
        currentGroupFacetName: currentGroupFacet.name,
        filtersDropdownOpen: filtersDropdownOpen,
        tempFilters: tempFilters,
        callBack: {
          dropdown: toggleDropdown,
          select: selectFilterOption,
          clear: clearFilters,
          apply: applyFilters
        }
      })), /*#__PURE__*/React.createElement("button", {
        className: 'button button__color--primary button__type--primary button__size--base button__icon searchPrompt__input-search-button',
        tabIndex: 0,
        onClick: function onClick() {
          return sendToResultsPage();
        }
      }, /*#__PURE__*/React.createElement("i", {
        className: 'icon__lg',
        "aria-hidden": 'true'
      }, "search"))), /*#__PURE__*/React.createElement("button", {
        className: 'button button__color--primary button__type--primary button__size--base button__fullWidth searchPrompt__input-search-button-mobile',
        onClick: function onClick() {
          return sendToResultsPage();
        }
      }, /*#__PURE__*/React.createElement("span", {
        className: 'searchPrompt__input-button-mobile-content'
      }, "Search", /*#__PURE__*/React.createElement("i", {
        className: 'icon__lg',
        "aria-hidden": 'true'
      }, "search")))), searchInput && ((autoCompletes === null || autoCompletes === void 0 ? void 0 : autoCompletes.items) || (autoCompletes === null || autoCompletes === void 0 ? void 0 : autoCompletes.suggestions)) ? ( /*#__PURE__*/React.createElement(AutoCompletes, {
        items: autoCompletes.items,
        suggestions: autoCompletes.suggestions,
        searchTerm: searchInput,
        suggestionsCallBack: setSearchInput
      })) : null), (currentQuickLinks === null || currentQuickLinks === void 0 ? void 0 : currentQuickLinks.links.length) && ( /*#__PURE__*/React.createElement(CurrentQuickLinks, {
        links: currentQuickLinks.links,
        label: currentQuickLinks.label
      }))));
    };

    return SearchPrompt;

})(React);
//# sourceMappingURL=SearchPrompt.js.map
