"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SearchController = void 0;
const search_service_1 = require("./search.service");
const service = new search_service_1.SearchService();
class SearchController {
    search = async (req, res) => {
        try {
            const q = String(req.query.q ?? "");
            const page = Number(req.query.page) || 1;
            const limit = Number(req.query.limit) || 12;
            const data = await service.search(q, page, limit);
            res.json({
                success: true,
                ...data,
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
}
exports.SearchController = SearchController;
