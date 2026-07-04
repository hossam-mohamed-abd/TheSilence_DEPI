"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const city_service_1 = __importDefault(require("./city.service"));
const bigintSerializer_1 = require("../../utils/bigintSerializer");
class CityController {
    async getByGovernorate(req, res) {
        try {
            const governorateId = Number(req.params.governorateId);
            const cities = await city_service_1.default.getByGovernorate(governorateId);
            res.json((0, bigintSerializer_1.serializeBigInt)(cities));
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
            const { name, governorateId, } = req.body;
            const city = await city_service_1.default.create(name, governorateId);
            res.status(201).json((0, bigintSerializer_1.serializeBigInt)({
                success: true,
                city,
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
exports.default = new CityController();
