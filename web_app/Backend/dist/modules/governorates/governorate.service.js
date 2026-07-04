"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const governorate_repository_1 = __importDefault(require("./governorate.repository"));
class GovernorateService {
    async getByCountry(countryId) {
        return governorate_repository_1.default.getByCountry(countryId);
    }
    async create(name, countryId) {
        return governorate_repository_1.default.create(name, countryId);
    }
}
exports.default = new GovernorateService();
