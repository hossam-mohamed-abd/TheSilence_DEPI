"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.authMiddleware = void 0;
const verifyToken_1 = require("../utils/verifyToken");
const authMiddleware = (req, res, next) => {
    try {
        const token = req.cookies.token;
        if (!token) {
            return res.status(401).json({
                success: false,
                message: 'Unauthorized'
            });
        }
        const payload = (0, verifyToken_1.verifyToken)(token);
        req.userId =
            payload.userId;
        next();
    }
    catch {
        return res.status(401).json({
            success: false,
            message: 'Invalid Token'
        });
    }
};
exports.authMiddleware = authMiddleware;
