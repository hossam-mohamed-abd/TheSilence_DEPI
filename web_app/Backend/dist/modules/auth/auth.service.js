"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const bcryptjs_1 = __importDefault(require("bcryptjs"));
const auth_repository_1 = __importDefault(require("./auth.repository"));
const generateToken_1 = require("../../utils/generateToken");
const notification_service_1 = require("../notifications/notification.service");
class AuthService {
    notificationService = new notification_service_1.NotificationService();
    async register(data) {
        const user = await auth_repository_1.default.findByEmail(data.email);
        if (user) {
            throw new Error("Email already exists");
        }
        const hashedPassword = await bcryptjs_1.default.hash(data.password, 10);
        const newUser = await auth_repository_1.default.create({
            first_name: data.firstName,
            last_name: data.lastName,
            email: data.email,
            password_hash: hashedPassword,
            phone: data.phone,
            role: "customer",
            is_active: true,
            cities: {
                connect: {
                    id: BigInt(data.cityId),
                },
            },
        });
        // 🔔 Welcome Notification
        await this.notificationService.createWelcomeNotification(newUser.id);
        const token = (0, generateToken_1.generateToken)(newUser.id);
        return {
            user: newUser,
            token,
        };
    }
    async login(data) {
        const user = await auth_repository_1.default.findByEmail(data.email);
        if (!user) {
            throw new Error("Invalid email or password");
        }
        const isPasswordCorrect = await bcryptjs_1.default.compare(data.password, user.password_hash);
        if (!isPasswordCorrect) {
            throw new Error("Invalid email or password");
        }
        const token = (0, generateToken_1.generateToken)(user.id);
        return {
            user,
            token,
        };
    }
    async profile(userId) {
        const user = await auth_repository_1.default.findById(BigInt(userId));
        if (!user) {
            throw new Error("User not found");
        }
        return user;
    }
}
exports.default = new AuthService();
