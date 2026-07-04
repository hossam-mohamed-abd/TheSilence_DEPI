"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const governorate_controller_1 = __importDefault(require("./governorate.controller"));
const router = (0, express_1.Router)();
router.get('/:countryId', governorate_controller_1.default.getByCountry);
router.post('/', governorate_controller_1.default.create);
exports.default = router;
