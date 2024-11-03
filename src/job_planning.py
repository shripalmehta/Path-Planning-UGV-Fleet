def create_repair_jobs(gdf, bot_capacity):
    jobs = []
    for idx, row in gdf.iterrows():
        material_required = row['material_required']
        job_count = 1
        while material_required > 0:
            amount = min(material_required, bot_capacity)
            jobs.append({
                'id': f"{idx}_{job_count}",
                'location': (row['geometry'].y, row['geometry'].x),
                'amount': amount
            })
            material_required -= amount
            job_count += 1
    return jobs