function ResourcesPage(){
    return(
        <div className="mt-20 space-y-">
    <h1 className="text-3xl font-semibold">Cybersecurity Resources</h1>
    <span className="text-gray-600">Simple cybersecurity resources for your protection.</span>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="max-w-sm rounded-xl overflow-hidden shadow-lg bg-white">
        <img className="w-full h-40 object-cover" src="https://i.pinimg.com/736x/7a/47/fd/7a47fd8b59f4efc546c148c46769ac92.jpg" />
        <div className="px-6 py-4">
            <div className="font-bold text-xl mb-2">Password Safety</div>
            <p className="text-gray-700">
            Learn how to create strong passwords and safely store them.
            </p>
        </div>
        <div className="px-6 pb-4 flex flex-wrap gap-2">
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#security</span>
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#passwords</span>
        </div>
        </div>

        <div className="max-w-sm rounded-xl overflow-hidden shadow-lg bg-white">
        <img className="w-full h-40 object-cover" src="https://i.pinimg.com/1200x/33/16/25/331625b650b4f641f0692481439eecef.jpg" />
        <div className="px-6 py-4">
            <div className="font-bold text-xl mb-2">Phishing Awareness</div>
            <p className="text-gray-700">
            Tips for spotting suspicious emails, links, and messages.
            </p>
        </div>
        <div className="px-6 pb-4 flex flex-wrap gap-2">
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#phishing</span>
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#emailSafety</span>
        </div>
        </div>

        <div className="max-w-sm rounded-xl overflow-hidden shadow-lg bg-white">
        <img className="w-full h-40 object-cover" src="https://i.pinimg.com/736x/4c/4e/e3/4c4ee31057582166f76e3695b3fdbfa5.jpg" />
        <div className="px-6 py-4">
            <div className="font-bold text-xl mb-2">Device Protection</div>
            <p className="text-gray-700">
            Keep your phone and laptop secure with simple steps.
            </p>
        </div>
        <div className="px-6 pb-4 flex flex-wrap gap-2">
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#devices</span>
            <span className="bg-gray-200 rounded-full px-3 py-1 text-xs font-semibold text-gray-700">#protection</span>
        </div>
        </div>
    </div>
</div>

    );
}
export default ResourcesPage;