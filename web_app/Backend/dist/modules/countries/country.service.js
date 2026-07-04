"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const country_repository_1 = __importDefault(require("./country.repository"));
class CountryService {
    async getAll() {
        return country_repository_1.default.getAll();
    }
}
exports.default = new CountryService();
