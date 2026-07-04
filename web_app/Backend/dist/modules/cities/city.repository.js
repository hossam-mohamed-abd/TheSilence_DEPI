"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const prisma_1 = __importDefault(require("../../config/prisma"));
class CityRepository {
    async getByGovernorate(governorateId) {
        return prisma_1.default.cities.findMany({
            where: {
                governorate_id: BigInt(governorateId),
            },
            orderBy: {
                name: 'asc',
            },
        });
    }
    async create(name, governorateId) {
        return prisma_1.default.cities.create({
            data: {
                name,
                governorates: {
                    connect: {
                        id: BigInt(governorateId),
                    },
                },
            },
        });
    }
}
exports.default = new CityRepository();
