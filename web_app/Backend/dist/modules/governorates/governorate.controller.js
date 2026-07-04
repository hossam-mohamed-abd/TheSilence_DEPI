"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const governorate_service_1 = __importDefault(require("./governorate.service"));
const bigintSerializer_1 = require("../../utils/bigintSerializer");
class GovernorateController {
    async getByCountry(req, res) {
        try {
            const countryId = Number(req.params.countryId);
            const governorates = await governorate_service_1.default.getByCountry(countryId);
            res.json((0, bigintSerializer_1.serializeBigInt)(governorates));
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }
    async create(req, res) {
        try {
            const { name, countryId, } = req.body;
            const governorate = await governorate_service_1.default.create(name, countryId);
            res.status(201).json((0, bigintSerializer_1.serializeBigInt)({
                success: true,
                governorate,
            }));
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }
}
exports.default = new GovernorateController();
