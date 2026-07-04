"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const helmet_1 = __importDefault(require("helmet"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
BigInt.prototype.toJSON = function () {
    return this.toString();
};
const auth_routes_1 = __importDefault(require("./modules/auth/auth.routes"));
const country_routes_1 = __importDefault(require("./modules/countries/country.routes"));
const governorate_routes_1 = __importDefault(require("./modules/governorates/governorate.routes"));
const city_routes_1 = __importDefault(require("./modules/cities/city.routes"));
const category_routes_1 = __importDefault(require("./modules/categories/category.routes"));
const medicine_routes_1 = __importDefault(require("./modules/medicines/medicine.routes"));
const favorite_routes_1 = __importDefault(require("./modules/favorites/favorite.routes"));
const pharmacy_routes_1 = __importDefault(require("./modules/pharmacies/pharmacy.routes"));
const statistics_routes_1 = __importDefault(require("./modules/statistics/statistics.routes"));
const notification_routes_1 = __importDefault(require("./modules/notifications/notification.routes"));
const search_routes_1 = __importDefault(require("./modules/search/search.routes"));
const app = (0, express_1.default)();
app.use((0, helmet_1.default)());
app.use((0, cors_1.default)({
    origin: ["http://localhost:4200", "https://medi-search-eight.vercel.app"],
    credentials: true,
}));
app.use(express_1.default.json());
app.use((0, cookie_parser_1.default)());
app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "MediSearch API Running",
    });
});
app.get("/api/health", (req, res) => {
    res.json({
        success: true,
        message: "Server is healthy",
    });
});
app.use("/api/auth", auth_routes_1.default);
app.use("/api/categories", category_routes_1.default);
app.use("/api/home/medicines", medicine_routes_1.default);
app.use("/api/favorites", favorite_routes_1.default);
app.use("/api/countries", country_routes_1.default);
app.use("/api/governorates", governorate_routes_1.default);
app.use("/api/cities", city_routes_1.default);
app.use("/api/home/pharmacies", pharmacy_routes_1.default);
app.use("/api/home/statistics", statistics_routes_1.default);
app.use("/api/notifications", notification_routes_1.default);
app.use("/api/search", search_routes_1.default);
exports.default = app;
