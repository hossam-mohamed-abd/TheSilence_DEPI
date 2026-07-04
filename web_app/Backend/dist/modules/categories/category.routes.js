"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const category_controller_1 = require("./category.controller");
const router = (0, express_1.Router)();
const controller = new category_controller_1.CategoryController();
router.get("/home", controller.getHomeCategories);
exports.default = router;
