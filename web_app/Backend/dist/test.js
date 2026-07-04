"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const prisma_1 = __importDefault(require("./config/prisma"));
async function test() {
    try {
        const users = await prisma_1.default.users.findMany();
        console.log(users);
    }
    catch (err) {
        console.log(err);
    }
}
test();
