"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PharmacyController = void 0;
const pharmacy_service_1 = require("./pharmacy.service");
const service = new pharmacy_service_1.PharmacyService();
class PharmacyController {
    async getFeaturedPharmacies(req, res) {
        try {
            const page = Number(req.query.page) || 1;
            const data = await service.getFeaturedPharmacies(page);
            res.json({
                success: true,
                data,
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }
    pharmacyService = new pharmacy_service_1.PharmacyService();
    getPharmacy = async (req, res) => {
        try {
            const id = BigInt(req.params.id);
            const pharmacy = await this.pharmacyService.getPharmacyDetails(id);
            return res.json({
                success: true,
                data: pharmacy,
            });
        }
        catch (error) {
            return res.status(404).json({
                success: false,
                message: error.message,
            });
        }
    };
    getPharmacyMedicines = async (req, res) => {
        try {
            const pharmacyId = BigInt(req.params.id);
            const page = Number(req.query.page) || 1;
            const limit = Number(req.query.limit) || 12;
            const search = String(req.query.search || "");
            const category = req.query.category
                ? BigInt(String(req.query.category))
                : undefined;
            const available = req.query.available === "true";
            const sort = String(req.query.sort || "name_asc");
            const result = await this.pharmacyService.getPharmacyMedicines(pharmacyId, {
                page,
                limit,
                search,
                category,
                available,
                sort,
            });
            return res.json({
                success: true,
                ...result,
            });
        }
        catch (error) {
            return res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
    getPharmacyCategories = async (req, res) => {
        try {
            const pharmacyId = BigInt(req.params.id);
            const data = await this.pharmacyService.getPharmacyCategories(pharmacyId);
            res.json({
                success: true,
                data,
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
    getPharmacyReviews = async (req, res) => {
        try {
            const pharmacyId = BigInt(req.params.id);
            const page = Number(req.query.page) || 1;
            const data = await this.pharmacyService.getPharmacyReviews(pharmacyId, page);
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
    getPharmacyStatistics = async (req, res) => {
        try {
            const pharmacyId = BigInt(req.params.id);
            const data = await this.pharmacyService.getPharmacyStatistics(pharmacyId);
            res.json({
                success: true,
                data,
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    };
    addReview = async (req, res) => {
        try {
            const pharmacyId = BigInt(req.params.id);
            const userId = BigInt(req.user.id);
            const { rating, review } = req.body;
            await this.pharmacyService.addReview(pharmacyId, userId, rating, review);
            res.status(201).json({
                success: true,
            });
        }
        catch (error) {
            res.status(400).json({
                success: false,
                message: error.message,
            });
        }
    };
}
exports.PharmacyController = PharmacyController;
