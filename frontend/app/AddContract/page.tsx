import React from "react";

const Page = () => {
	const handleSubmit = () => {
		console.log("File submitted");
	};

	return (
		<div
			id="main-container"
			className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900"
		>
			<form
				action=""
				className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg"
			>
				<div className="flex flex-col">
					<div className="flex gap-4">
						<label
							htmlFor="client-name"
							className="text-black dark:text-white align-middle pt-2"
						>
							Client Name
						</label>
						<input
							id="client-name"
							className="rounded p-2 border border-gray-300 dark:border-gray-700"
							type="text"
						/>
					</div>

          <div className="flex gap-4">
						<label
							htmlFor="client-name"
							className="text-black dark:text-white align-middle pt-2"
						>
							Document Name
						</label>
						<input
							id="doc-name"
							className="rounded p-2 border border-gray-300 dark:border-gray-700"
							type="text"
						/>
					</div>


				</div>
			</form>
		</div>
	);
};

export default Page;
