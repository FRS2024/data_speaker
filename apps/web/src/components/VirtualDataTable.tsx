import React, { useMemo, useRef, useState } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  ColumnDef,
  flexRender,
  SortingState,
} from "@tanstack/react-table";
import { useVirtualizer } from "@tanstack/react-virtual";
import { DatasetColumn } from "@/lib/types";

interface VirtualDataTableProps {
  columns: DatasetColumn[];
  data: Record<string, any>[];
  totalRows?: number;
  tableName?: string;
  onExport?: (format: string) => void;
  isLoading?: boolean;
}

export const VirtualDataTable: React.FC<VirtualDataTableProps> = ({
  columns: rawColumns,
  data,
  totalRows,
  tableName = "active_dataset",
  onExport,
  isLoading = false,
}) => {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState<string>("");
  const tableContainerRef = useRef<HTMLDivElement>(null);

  // Map dtype to Stitch pill color
  const getTypeBadgeColor = (type: string) => {
    const t = (type || "").toLowerCase();
    if (t.includes("int") || t.includes("long")) return "bg-primary-container/20 text-primary";
    if (t.includes("float") || t.includes("double") || t.includes("numeric") || t.includes("decimal"))
      return "bg-tertiary-container/20 text-tertiary";
    if (t.includes("date") || t.includes("time")) return "bg-secondary-container/30 text-secondary";
    if (t.includes("bool")) return "bg-primary/20 text-primary-fixed";
    return "bg-surface-container-highest text-on-surface-variant";
  };

  // Build TanStack Table column definitions
  const tableColumns = useMemo<ColumnDef<Record<string, any>>[]>(() => {
    if (!rawColumns || rawColumns.length === 0) return [];

    const indexCol: ColumnDef<Record<string, any>> = {
      id: "_row_index",
      header: "#",
      size: 56,
      cell: (info) => (
        <span className="text-outline text-[12px] group-hover:text-on-surface-variant select-none">
          {info.row.index + 1}
        </span>
      ),
    };

    const dataCols: ColumnDef<Record<string, any>>[] = rawColumns.map((col) => ({
      accessorKey: col.name,
      header: () => (
        <div className="flex items-center gap-1.5 py-0.5 select-none">
          <span className="text-on-surface font-medium truncate">{col.name}</span>
          <span
            className={`px-1.5 py-0.5 rounded text-[10px] font-label-caps uppercase ${getTypeBadgeColor(
              col.type
            )}`}
          >
            {col.type || "ANY"}
          </span>
        </div>
      ),
      cell: (info) => {
        const val = info.getValue();
        if (val === null || val === undefined) {
          return <span className="text-outline/40 italic font-mono text-[12px]">null</span>;
        }
        if (typeof val === "boolean") {
          return (
            <span
              className={`px-1.5 py-0.5 rounded text-[11px] font-mono font-medium ${
                val ? "bg-tertiary/20 text-tertiary" : "bg-error/20 text-error"
              }`}
            >
              {val ? "TRUE" : "FALSE"}
            </span>
          );
        }
        if (typeof val === "number") {
          return (
            <span className="font-code-tabular text-on-surface">
              {val.toLocaleString(undefined, { maximumFractionDigits: 4 })}
            </span>
          );
        }
        return <span className="font-code-tabular text-on-surface-variant truncate block">{String(val)}</span>;
      },
    }));

    return [indexCol, ...dataCols];
  }, [rawColumns]);

  const table = useReactTable({
    data,
    columns: tableColumns,
    state: {
      sorting,
      globalFilter,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  const { rows } = table.getRowModel();

  // Headless Row Virtualizer with absolute positioning
  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => 38,
    overscan: 25,
  });

  const virtualRows = rowVirtualizer.getVirtualItems();
  const totalHeight = rowVirtualizer.getTotalSize();

  return (
    <div className="flex flex-col h-full w-full bg-surface-container-lowest overflow-hidden">
      {/* Top Table Action & Filter Toolbar */}
      <div className="px-space-md py-2.5 bg-surface-container-low border-b border-outline-variant/30 flex flex-wrap items-center justify-between gap-space-sm shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant font-code-tabular text-code-tabular text-[12px]">
            <span className="material-symbols-outlined text-[15px] text-primary">table_chart</span>
            <span className="text-on-surface font-medium">{tableName}</span>
          </div>
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant font-code-tabular text-code-tabular text-[12px]">
            <span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
            <span>
              <strong className="text-on-surface font-semibold">
                {rows.length.toLocaleString()}
              </strong>{" "}
              / {totalRows ? totalRows.toLocaleString() : data.length.toLocaleString()} rows
            </span>
          </div>
          {isLoading && (
            <span className="flex items-center gap-1 text-[12px] text-secondary animate-pulse">
              <span className="material-symbols-outlined text-[14px]">sync</span>
              <span>Syncing rows...</span>
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Search Filter Input */}
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant focus-within:text-on-surface focus-within:ring-1 focus-within:ring-primary/40 transition-all text-[12px]">
            <span className="material-symbols-outlined text-[15px] text-outline">filter_list</span>
            <input
              type="text"
              value={globalFilter ?? ""}
              onChange={(e) => setGlobalFilter(e.target.value)}
              placeholder="Search table..."
              className="bg-transparent text-on-surface placeholder:text-outline focus:outline-none w-32 sm:w-44 text-body-sm"
            />
            {globalFilter && (
              <button
                onClick={() => setGlobalFilter("")}
                className="hover:text-on-surface text-outline transition-colors"
              >
                <span className="material-symbols-outlined text-[13px]">close</span>
              </button>
            )}
          </div>

          {/* Export Dropdown / Trigger */}
          {onExport && (
            <div className="flex items-center gap-1">
              <button
                onClick={() => onExport("csv")}
                className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface text-[12px] font-code-tabular transition-colors"
                title="Export CSV"
              >
                <span className="material-symbols-outlined text-[14px]">download</span>
                <span>CSV</span>
              </button>
              <button
                onClick={() => onExport("parquet")}
                className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface text-[12px] font-code-tabular transition-colors"
                title="Export Parquet"
              >
                <span className="material-symbols-outlined text-[14px]">download</span>
                <span>Parquet</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Virtual Table Scroll Container */}
      <div
        ref={tableContainerRef}
        className="flex-1 overflow-auto relative bg-surface-container-lowest select-text"
        style={{ willChange: "transform" }}
      >
        <table className="w-full text-left font-code-tabular text-code-tabular text-[13px] border-collapse">
          {/* Sticky Header Strip */}
          <thead className="sticky top-0 bg-[#1c1b1c]/95 backdrop-blur-md z-20 shadow-sm border-b border-outline-variant/30 select-none">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  const canSort = header.column.getCanSort() && header.id !== "_row_index";
                  const sortDir = header.column.getIsSorted();

                  return (
                    <th
                      key={header.id}
                      className="py-2.5 px-3.5 font-normal text-on-surface-variant border-r border-outline-variant/20 last:border-r-0"
                      style={{ width: header.getSize() }}
                    >
                      <div
                        className={`flex items-center justify-between gap-1.5 ${
                          canSort ? "cursor-pointer hover:text-on-surface" : ""
                        }`}
                        onClick={canSort ? header.column.getToggleSortingHandler() : undefined}
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {canSort && (
                          <span className="material-symbols-outlined text-[14px] text-outline shrink-0">
                            {sortDir === "asc"
                              ? "arrow_upward"
                              : sortDir === "desc"
                              ? "arrow_downward"
                              : "unfold_more"}
                          </span>
                        )}
                      </div>
                    </th>
                  );
                })}
              </tr>
            ))}
          </thead>

          {/* Virtual Rows with absolute translateY rendering */}
          <tbody
            className="relative"
            style={{
              height: `${totalHeight}px`,
            }}
          >
            {virtualRows.length === 0 ? (
              <tr>
                <td
                  colSpan={tableColumns.length}
                  className="py-16 text-center text-outline font-body-md"
                >
                  {data.length === 0 ? "No dataset records found." : "No records match search criteria."}
                </td>
              </tr>
            ) : (
              virtualRows.map((virtualRow) => {
                const row = rows[virtualRow.index];
                const isEven = virtualRow.index % 2 === 0;

                return (
                  <tr
                    key={row.id}
                    data-index={virtualRow.index}
                    className={`absolute left-0 right-0 flex w-full items-center transition-colors group hover:bg-surface-container-high/60 ${
                      isEven ? "bg-surface-container-lowest" : "bg-[#161617]"
                    } border-b border-outline-variant/15`}
                    style={{
                      height: `${virtualRow.size}px`,
                      transform: `translateY(${virtualRow.start}px)`,
                    }}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <td
                        key={cell.id}
                        className="py-2 px-3.5 border-r border-outline-variant/15 last:border-r-0 overflow-hidden text-ellipsis whitespace-nowrap flex items-center"
                        style={{ width: cell.column.getSize(), flex: cell.column.id === "_row_index" ? "0 0 56px" : 1 }}
                      >
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Bottom Table Footer Summary */}
      <div className="px-space-md py-1.5 bg-surface-container-low border-t border-outline-variant/25 flex items-center justify-between text-[11px] font-code-tabular text-outline shrink-0">
        <div className="flex items-center gap-3">
          <span>
            Displaying <strong className="text-on-surface">{rows.length}</strong> items
          </span>
          <span>•</span>
          <span className="text-tertiary">Headless TanStack Virtual 60 FPS</span>
        </div>
        <div className="flex items-center gap-2">
          <span>Memory: ~{(data.length * 0.08).toFixed(1)} KB cached</span>
        </div>
      </div>
    </div>
  );
};
