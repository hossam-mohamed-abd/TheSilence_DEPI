"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const prisma_1 = __importDefault(require("../../config/prisma"));
class CountryRepository {
    async getAll() {
        return prisma_1.default.countries.findMany({
            orderBy: {
                name: 'asc'
            }
        });
    }
}
exports.default = new CountryRepository();
