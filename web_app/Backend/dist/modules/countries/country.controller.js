"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const country_service_1 = __importDefault(require("./country.service"));
const bigintSerializer_1 = require("../../utils/bigintSerializer");
class CountryController {
    async getAll(req, res) {
        const countries = await country_service_1.default.getAll();
        res.json((0, bigintSerializer_1.serializeBigInt)(countries));
    }
}
exports.default = new CountryController();
