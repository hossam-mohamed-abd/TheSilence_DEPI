import prisma from "../../config/prisma";

export class MedicineRepository {
  async getFeaturedMedicines(page: number) {
    const skip = Math.max(page - 1, 0);

    const categories = await prisma.drug_categories.findMany({
      take: 4,
      skip: (page - 1) * 4,
      select: {
        id: true,
      },
      orderBy: {
        name: "asc",
      },
    });

    const medicines = await Promise.all(
      categories.map(async (category) => {
        const medicine = await prisma.drugs.findFirst({
          where: {
            category_id: category.id,
          },

          skip,

          take: 1,

          orderBy: {
            name: "asc",
          },

          include: {
            drug_categories: true,

            pharmacy_inventory: {
              select: {
                price: true,
                pharmacy_id: true,
              },
            },

            drug_alternatives_drug_alternatives_drug_idTodrugs: {
              select: {
                id: true,
              },
            },
          },
        });

        return medicine;
      }),
    );

    const filtered = medicines.filter(Boolean).map((drug: any) => {
      const prices = drug.pharmacy_inventory
        .map((p: any) => Number(p.price))
        .filter((price: number) => !isNaN(price));

      return {
        id: Number(drug.id),

        name: drug.name,

        active_substance: drug.active_substance,

        dosage_form: drug.dosage_form,

        strength: drug.strength,

        manufacturer: drug.manufacturer,

        description: drug.description,

        image_url: drug.image_url,

        category_name: drug.drug_categories?.name,

        min_price: prices.length ? Math.min(...prices) : undefined,

        pharmacy_count: drug.pharmacy_inventory.length,

        alternatives_count:
          drug.drug_alternatives_drug_alternatives_drug_idTodrugs.length,

        is_available: drug.pharmacy_inventory.length > 0,

        is_favorite: false,
      };
    });

    return {
      medicines: filtered,
      hasMore: filtered.length > 0,
    };
  }
}
