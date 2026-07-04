"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const auth_service_1 = __importDefault(require("./auth.service"));
const bigintSerializer_1 = require("../../utils/bigintSerializer");
class AuthController {
    async register(req, res) {
        console.log(req.body);
        try {
            const result = await auth_service_1.default.register(req.body);
            res.cookie("token", result.token, {
                httpOnly: true,
                secure: process.env.NODE_ENV === "production",
                sameSite: "lax",
                maxAge: 7 * 24 * 60 * 60 * 1000,
            });
            res.status(201).json({
                success: true,
                user: (0, bigintSerializer_1.serializeBigInt)(result.user),
            });
        }
        catch (error) {
            res.status(400).json({
                success: false,
                message: error.message,
            });
        }
    }
    async login(req, res) {
        try {
            const result = await auth_service_1.default.login(req.body);
            const isProduction = process.env.NODE_ENV === "production";
            res.cookie("token", result.token, {
                httpOnly: true,
                secure: isProduction,
                sameSite: isProduction ? "none" : "lax",
                maxAge: 7 * 24 * 60 * 60 * 1000,
            });
            res.status(200).json((0, bigintSerializer_1.serializeBigInt)({
                success: true,
                user: result.user,
            }));
        }
        catch (error) {
            res.status(400).json({
                success: false,
                message: error.message,
            });
        }
    }
    async profile(req, res) {
        try {
            const user = await auth_service_1.default.profile(req.userId);
            res.json((0, bigintSerializer_1.serializeBigInt)({
                success: true,
                user,
            }));
        }
        catch (error) {
            res.status(404).json({
                success: false,
                message: error.message,
            });
        }
    }
    async logout(req, res) {
        const isProduction = process.env.NODE_ENV === "production";
        res.clearCookie("token", {
            httpOnly: true,
            secure: isProduction,
            sameSite: isProduction ? "none" : "lax",
        });
        res.status(200).json({
            success: true,
            message: "Logged out successfully",
        });
    }
}
exports.default = new AuthController();
