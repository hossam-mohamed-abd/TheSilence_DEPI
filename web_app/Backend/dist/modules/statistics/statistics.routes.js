"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const statistics_controller_1 = require("./statistics.controller");
const router = (0, express_1.Router)();
const controller = new statistics_controller_1.StatisticsController();
router.get('/', controller.getStatistics);
exports.default = router;
