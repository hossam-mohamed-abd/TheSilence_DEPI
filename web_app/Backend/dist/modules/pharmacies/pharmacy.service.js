"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PharmacyService = void 0;
const pharmacy_repository_1 = require("./pharmacy.repository");
class PharmacyService {
    repository = new pharmacy_repository_1.PharmacyRepository();
    async getFeaturedPharmacies(page) {
        return this.repository.getFeaturedPharmacies(page);
    }
    pharmacyRepository = new pharmacy_repository_1.PharmacyRepository();
    async getPharmacyDetails(pharmacyId) {
        const pharmacy = await this.pharmacyRepository.findById(pharmacyId);
        if (!pharmacy) {
            throw new Error("Pharmacy not found");
        }
        const ratings = pharmacy.pharmacy_ratings.map((r) => r.rating ?? 0);
        const avgRating = ratings.length
            ? ratings.reduce((a, b) => a + b, 0) / ratings.length
            : 0;
        const availableCount = pharmacy.pharmacy_inventory.filter((item) => (item.quantity ?? 0) > 0).length;
        const categories = new Set(pharmacy.pharmacy_inventory
            .map((item) => item.drugs?.category_id)
            .filter(Boolean));
        return {
            id: Number(pharmacy.id),
            name: pharmacy.name,
            image_url: pharmacy.logo_url,
            phone: pharmacy.phone,
            email: pharmacy.email,
            address: pharmacy.address,
            city: pharmacy.cities?.name,
            governorate: pharmacy.cities?.governorates?.name,
            rating: Number(avgRating.toFixed(1)),
            reviews_count: ratings.length,
            medicines_count: pharmacy.pharmacy_inventory.length,
            available_count: availableCount,
            categories_count: categories.size,
        };
    }
    async getPharmacyMedicines(pharmacyId, options) {
        return this.pharmacyRepository.findMedicines(pharmacyId, options);
    }
    async getPharmacyCategories(pharmacyId) {
        return this.pharmacyRepository.findCategories(pharmacyId);
    }
    async getPharmacyReviews(pharmacyId, page) {
        return this.pharmacyRepository.findReviews(pharmacyId, page);
    }
    async addReview(pharmacyId, userId, rating, review) {
        return this.pharmacyRepository.createReview(pharmacyId, userId, rating, review);
    }
    async getPharmacyStatistics(pharmacyId) {
        return this.pharmacyRepository.getStatistics(pharmacyId);
    }
}
exports.PharmacyService = PharmacyService;
