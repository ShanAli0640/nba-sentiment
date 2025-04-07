import { getPlayerDetails, getPlayerIDList } from '@/app/lib/players';

export async function generateStaticParams() {
    const players = await getPlayerIDList();
    return players.map((player) => ({
        playerName: player.name
    }));
}

export default async function Post({ params }) {
    const playerData = await getPlayerDetails(params.playerName)
    return (
        <div className='bg-gray-800 h-screen p-16 text-gray-100'>
            <div className='text-center font-bold text-3xl'>
                {playerData.name}
            </div>
            <div className='text-center'>
                {playerData.description}
            </div>
        </div>
    );
}