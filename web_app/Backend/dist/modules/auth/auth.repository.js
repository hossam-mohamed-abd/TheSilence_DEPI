"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const prisma_1 = __importDefault(require("../../config/prisma"));
class AuthRepository {
    async findByEmail(email) {
        return prisma_1.default.users.findUnique({
            where: {
                email,
            },
        });
    }
    async create(data) {
        return prisma_1.default.users.create({
            data,
        });
    }
    async findById(id) {
        return prisma_1.default.users.findUnique({
            where: {
                id,
            },
        });
    }
}
exports.default = new AuthRepository();
