"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const prisma_1 = __importDefault(require("../../config/prisma"));
class GovernorateRepository {
    async getByCountry(countryId) {
        return prisma_1.default.governorates.findMany({
            where: {
                country_id: BigInt(countryId),
            },
            orderBy: {
                name: 'asc',
            },
        });
    }
    async create(name, countryId) {
        return prisma_1.default.governorates.create({
            data: {
                name,
                countries: {
                    connect: {
                        id: BigInt(countryId),
                    },
                },
            },
        });
    }
}
exports.default = new GovernorateRepository();
