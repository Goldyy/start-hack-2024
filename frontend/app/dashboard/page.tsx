import { getOvoHunters } from '@/lib/data/model/ovo-hunter'
import OvoHuntersTable from '@/components/dashboard/OvoHuntersTable';
import { AddHunterDialog } from '@/components/dashboard/AddHunterDialog';


export default async function Page() {
    const ovoHunters = await getOvoHunters();
    console.log(ovoHunters);

    return (
    <div>
        <div className="flex justify-between">
            <p>Dashboard</p>
            <AddHunterDialog />
        </div>

        <OvoHuntersTable data={ovoHunters} />
    </div>
    )
}