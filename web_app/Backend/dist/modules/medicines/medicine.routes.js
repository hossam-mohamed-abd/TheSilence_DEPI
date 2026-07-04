"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const medicine_controller_1 = require("./medicine.controller");
const router = (0, express_1.Router)();
const controller = new medicine_controller_1.MedicineController();
router.get("/featured", controller.getFeaturedMedicines);
exports.default = router;
