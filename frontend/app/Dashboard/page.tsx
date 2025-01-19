import tableData from "@/_Data/table-data";
import { FileUploader } from "@/components/FileUpload";
import Button from "@/components/Button";

const Page = () => {

  const data = tableData.map((res, index) => {
		const signedOnDate = res["signed-on"].toLocaleDateString();
		const expiringOnDate = res["expiry-on"].toLocaleDateString();
		return (
			<tr key={index}>
				<td className="px-6 py-3 text-center align-middle">
					{res["client-name"]}
				</td>
				<td className="px-6 py-3 text-center align-middle">
					{res["doc-name"]}
				</td>
				<td className="px-6 py-3 text-center align-middle">{res["email"]}</td>
				<td className="px-6 py-3 text-center align-middle">{expiringOnDate}</td>
				<td className="px-6 py-3 text-center align-middle">{res["email"]}</td>
			</tr>
		);
	});

	return (
		<div className="min-h-screen w-full bg-neutral-900 items-center justify-center p-4">
			<FileUploader />
			<div className="w-full max-w-full bg-neutral-900 p-6 rounded-lg shadow-md overflow-auto">
				<table className="min-w-full table-auto border-collapse border border-neutral-700 text-white">
					<thead>
						<tr className="bg-gray-800 text-gray-100">
							<th className="px-6 py-3">Client Name</th>
							<th className="px-6 py-3">Document</th>
							<th className="px-6 py-3">Signed On</th>
							<th className="px-6 py-3">Valid Till</th>
							<th className="px-6 py-3">Email</th>
						</tr>
					</thead>
					<tbody>{data}</tbody>
				</table>
			</div>
      {/* <Button buttonText="Add Contract" path="AddContract"/> */}
		</div>
	);
};

export default Page;
