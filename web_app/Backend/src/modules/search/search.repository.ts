import prisma from "../../config/prisma";

export class SearchRepository {
  async search(q: string, page: number, limit: number) {
    const skip = (page - 1) * limit;

    const where =
      q.trim() === ""
        ? {}
        : {
            OR: [
              {
                name: {
                  contains: q,
                  mode: "insensitive" as const,
                },
              },
              {
                active_substance: {
                  contains: q,
                  mode: "insensitive" as const,
                },
              },
              {
                manufacturer: {
                  contains: q,
                  mode: "insensitive" as const,
                },
              },
            ],
          };

    const total = await prisma.drugs.count({
      where,
    });

    const drugs = await prisma.drugs.findMany({
      where,

      skip,

      take: limit,

      include: {
        drug_categories: true,

        pharmacy_inventory: {
          select: {
            price: true,
            quantity: true,
            pharmacy_id: true,
          },
        },

        drug_alternatives_drug_alternatives_drug_idTodrugs: true,
      },

      orderBy: {
        name: "asc",
      },
    });

    const data = drugs.map((drug) => {
      const prices = drug.pharmacy_inventory
        .map((p) => Number(p.price))
        .filter((p) => !isNaN(p));

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

        is_available: drug.pharmacy_inventory.some(
          (p) => (p.quantity ?? 0) > 0,
        ),

        is_favorite: false,
      };
    });

    return {
      page,
      limit,
      total,
      hasMore: skip + limit < total,
      data,
    };
  }
}
