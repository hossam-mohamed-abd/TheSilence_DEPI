"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MedicineController = void 0;
const medicine_service_1 = require("./medicine.service");
class MedicineController {
    medicineService = new medicine_service_1.MedicineService();
    getFeaturedMedicines = async (req, res) => {
        try {
            const page = Number(req.query.page || 1);
            const result = await this
                .medicineService
                .getFeaturedMedicines(page);
            return res.json({
                success: true,
                hasMore: result.hasMore,
                data: result.medicines,
            });
        }
        catch (error) {
            console.error(error);
            return res
                .status(500)
                .json({
                success: false,
                message: error.message,
            });
        }
    };
}
exports.MedicineController = MedicineController;
