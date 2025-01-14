import React from 'react';

const Table = ({ data, columns, title }) => {
  return (
    <div className="relative overflow-x-auto p-4">
      {title && <h1 className="text-xl font-bold mb-4">{title}</h1>}
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            {columns.map((col, index) => (
              <th
                key={index}
                className="border border-gray-300 px-4 py-2 text-left font-semibold"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50">
              {columns.map((col, colIndex) => (
                <td
                  key={colIndex}
                  className={`border border-gray-300 px-4 py-2 ${
                    col.cellStyle ? col.cellStyle(row[col.accessor]) : ''
                  }`}
                >
                  {col.render ? col.render(row[col.accessor], row) : row[col.accessor]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
