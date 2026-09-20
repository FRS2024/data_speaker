import React, { useState, useEffect, useMemo, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { SchemaResponse, ForeignKeyRelation } from "@/lib/types";
import { fetchTableRelations, saveSqlCheckpoint } from "@/lib/api";

interface SchemaMapperProps {
  sessionId: string;
  schema?: SchemaResponse;
  onNavigateTab?: (tab: string) => void;
  onExecuteSql?: (sql: string) => void;
  onSendToChat?: (prompt: string) => void;
}

interface UserJoinLink {
  id: string;
  fromTable: string;
  fromColumn: string;
  toTable: string;
  toColumn: string;
  joinType: "INNER JOIN" | "LEFT JOIN" | "RIGHT JOIN" | "FULL OUTER JOIN";
}

export const SchemaMapper: React.FC<SchemaMapperProps> = ({
  sessionId,
  schema,
  onNavigateTab,
  onExecuteSql,
  onSendToChat,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeJoinType, setActiveJoinType] = useState<
    "INNER JOIN" | "LEFT JOIN" | "RIGHT JOIN" | "FULL OUTER JOIN"
  >("INNER JOIN");
  const [selectedPort, setSelectedPort] = useState<{ table: string; column: string } | null>(null);
  const [userLinks, setUserLinks] = useState<UserJoinLink[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  // Fetch inferred relationships from API
  const { data: relationsData, isLoading: relationsLoading } = useQuery({
    queryKey: ["relations", sessionId],
    queryFn: () => fetchTableRelations(sessionId),
    enabled: Boolean(sessionId),
  });

  // Initialize links with inferred relations
  useEffect(() => {
    if (relationsData?.relations && userLinks.length === 0) {
      const initial = relationsData.relations.map((rel: ForeignKeyRelation, idx: number) => ({
        id: `rel_${idx}`,
        fromTable: rel.from_table,
        fromColumn: rel.from_column,
        toTable: rel.to_table,
        toColumn: rel.to_column,
        joinType: rel.suggested_join_type,
      }));
      setUserLinks(initial);
    }
  }, [relationsData?.relations]);

  const tables = schema?.profiles || [];

  // Handle clicking on a column port to create a link
  const handlePortClick = (table: string, column: string) => {
    if (!selectedPort) {
      setSelectedPort({ table, column });
    } else {
      if (selectedPort.table === table) {
        // Cancel or switch selection within same table
        setSelectedPort({ table, column });
        return;
      }

      // Create new join link between selectedPort and clicked port
      const newLink: UserJoinLink = {
        id: `link_${Date.now()}`,
        fromTable: selectedPort.table,
        fromColumn: selectedPort.column,
        toTable: table,
        toColumn: column,
        joinType: activeJoinType,
      };

      setUserLinks((prev) => [...prev, newLink]);
      setSelectedPort(null);
    }
  };

  const handleRemoveLink = (linkId: string) => {
    setUserLinks((prev) => prev.filter((l) => l.id !== linkId));
  };

  // Generate live SQL query from active links
  const generatedSql = useMemo(() => {
    if (tables.length === 0) return "-- Upload datasets to map schemas";
    if (userLinks.length === 0) {
      const primary = tables[0].table_name;
      return `-- Single Table View\nSELECT * FROM "${primary}" LIMIT 1000;`;
    }

    const firstLink = userLinks[0];
    const baseTable = firstLink.fromTable;
    let sql = `SELECT\n`;

    // Select qualified columns
    const selectCols: string[] = [];
    const fromProf = tables.find((t) => t.table_name === baseTable);
    if (fromProf) {
      fromProf.columns.slice(0, 5).forEach((c) => {
        selectCols.push(`  "${baseTable}"."${c.name}" AS "${baseTable}_${c.name}"`);
      });
    }

    userLinks.forEach((link) => {
      const targetProf = tables.find((t) => t.table_name === link.toTable);
      if (targetProf) {
        targetProf.columns.slice(0, 5).forEach((c) => {
          selectCols.push(`  "${link.toTable}"."${c.name}" AS "${link.toTable}_${c.name}"`);
        });
      }
    });

    sql += (selectCols.length > 0 ? selectCols.join(",\n") : `  *`) + `\nFROM "${baseTable}"\n`;

    userLinks.forEach((link) => {
      sql += `${link.joinType} "${link.toTable}"\n  ON "${link.fromTable}"."${link.fromColumn}" = "${link.toTable}"."${link.toColumn}"\n`;
    });

    sql += `LIMIT 5000;`;
    return sql;
  }, [tables, userLinks]);

  const handleSaveJoinedCheckpoint = async () => {
    if (!sessionId || !generatedSql) return;
    setIsSaving(true);
    setSaveMessage(null);
    try {
      const res = await saveSqlCheckpoint(
        sessionId,
        generatedSql,
        undefined,
        `Joined view generated via Schema Mapper`
      );
      setSaveMessage(`Created checkpoint ${res.version_tag} (${res.row_count} rows).`);
      setTimeout(() => setSaveMessage(null), 4000);
    } catch (e: any) {
      setSaveMessage(`Error: ${e.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div
      ref={containerRef}
      className="flex flex-col h-[calc(100vh-4rem)] w-full bg-[#131314] overflow-hidden select-none relative"
    >
      {/* Top Controls Toolbar */}
      <div className="h-12 px-space-md bg-surface-container-lowest border-b border-outline-variant/20 flex items-center justify-between shrink-0 z-20">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-on-surface-variant font-code-tabular text-[12px] border border-outline-variant/30">
            <span className="material-symbols-outlined text-[16px] text-tertiary">hub</span>
            <span className="text-on-surface font-medium">Interactive Relational Schema Mapper</span>
          </div>

          <div className="flex items-center gap-1 bg-surface-container-lowest p-1 rounded-lg border border-outline-variant/20 text-xs">
            {(["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"] as const).map((type) => (
              <button
                key={type}
                onClick={() => setActiveJoinType(type)}
                className={`px-2.5 py-1 rounded text-[11px] font-medium transition ${
                  activeJoinType === type
                    ? "bg-tertiary/20 text-tertiary border border-tertiary/30"
                    : "text-outline hover:text-on-surface hover:bg-surface-container"
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Port Alert / Helper */}
        <div className="flex items-center gap-3">
          {selectedPort && (
            <div className="flex items-center gap-1.5 text-xs text-primary bg-primary/10 px-2.5 py-1 rounded border border-primary/20 animate-pulse">
              <span className="material-symbols-outlined text-[14px]">link</span>
              <span>
                Click a column in another table to connect from{" "}
                <strong>{selectedPort.table}.{selectedPort.column}</strong>
              </span>
              <button
                onClick={() => setSelectedPort(null)}
                className="ml-1 hover:text-error text-outline text-[12px]"
              >
                ✕
              </button>
            </div>
          )}

          {saveMessage && (
            <div className="text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/30">
              {saveMessage}
            </div>
          )}
        </div>
      </div>

      {/* Main Canvas Area */}
      <div className="flex-1 w-full overflow-auto p-8 relative flex flex-wrap gap-8 items-start justify-center">
        {tables.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-96 text-outline font-mono text-center space-y-3">
            <span className="material-symbols-outlined text-4xl text-outline/40">table_chart_view</span>
            <div className="text-sm font-medium text-on-surface">No Multi-Table Datasets Uploaded</div>
            <p className="text-xs max-w-sm">
              Upload CSV, Parquet, or SQLite files in the upload modal to visually map schemas,
              join keys, and build multi-table queries.
            </p>
          </div>
        ) : (
          tables.map((table) => {
            const hasJoinedColumns = userLinks.some(
              (l) => l.fromTable === table.table_name || l.toTable === table.table_name
            );

            return (
              <div
                key={table.table_name}
                className="w-80 bg-surface-container-low rounded-xl border border-outline-variant/30 shadow-2xl overflow-hidden flex flex-col z-10 transition-all hover:border-outline-variant/60"
              >
                {/* Table Card Header */}
                <div className="px-4 py-3 bg-surface-container border-b border-outline-variant/20 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-tertiary text-[18px]">table_rows</span>
                    <span className="font-mono text-xs font-bold text-on-surface truncate">
                      {table.table_name}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 text-[10px] font-mono text-outline">
                    <span className="px-1.5 py-0.5 rounded bg-surface-container-high border border-outline-variant/20">
                      {table.row_count.toLocaleString()} rows
                    </span>
                  </div>
                </div>

                {/* Column Port Rows */}
                <div className="divide-y divide-outline-variant/10 max-h-80 overflow-y-auto">
                  {table.columns.map((col) => {
                    const isId =
                      col.name.toLowerCase().endsWith("_id") ||
                      col.name.toLowerCase() === "id" ||
                      col.name.toLowerCase().includes("key");
                    const isSelected =
                      selectedPort?.table === table.table_name &&
                      selectedPort?.column === col.name;
                    const isLinked = userLinks.some(
                      (l) =>
                        (l.fromTable === table.table_name && l.fromColumn === col.name) ||
                        (l.toTable === table.table_name && l.toColumn === col.name)
                    );

                    return (
                      <div
                        key={col.name}
                        onClick={() => handlePortClick(table.table_name, col.name)}
                        className={`px-3 py-2 flex items-center justify-between group cursor-pointer transition ${
                          isSelected
                            ? "bg-primary/20 text-primary"
                            : isLinked
                            ? "bg-tertiary/10 text-tertiary hover:bg-tertiary/20"
                            : "hover:bg-surface-container text-on-surface-variant"
                        }`}
                      >
                        <div className="flex items-center gap-2 truncate">
                          <span
                            className={`material-symbols-outlined text-[14px] ${
                              isId ? "text-amber-400" : "text-outline/40"
                            }`}
                          >
                            {isId ? "key" : "drag_handle"}
                          </span>
                          <span className="font-mono text-xs font-medium truncate">{col.name}</span>
                        </div>

                        <div className="flex items-center gap-1.5 shrink-0">
                          <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-surface-container text-outline">
                            {col.dtype}
                          </span>
                          <button
                            title="Click to link column"
                            className={`w-4 h-4 rounded-full border flex items-center justify-center transition ${
                              isSelected
                                ? "bg-primary border-primary text-black"
                                : isLinked
                                ? "bg-tertiary border-tertiary text-black"
                                : "border-outline/40 group-hover:border-primary group-hover:bg-primary/20"
                            }`}
                          >
                            <span className="text-[10px] leading-none">●</span>
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Bottom SQL Dock & Action Strip */}
      <div className="bg-surface-container-lowest border-t border-outline-variant/30 p-4 shrink-0 z-20 flex flex-col gap-3">
        {/* Active Relationships Tags */}
        {userLinks.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-outline font-mono text-[11px]">ACTIVE JOINS:</span>
            {userLinks.map((link) => (
              <div
                key={link.id}
                className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container border border-outline-variant/30 text-tertiary font-mono text-[11px]"
              >
                <span>
                  {link.fromTable}.{link.fromColumn}
                </span>
                <span className="text-outline font-bold text-[9px]">{link.joinType}</span>
                <span>
                  {link.toTable}.{link.toColumn}
                </span>
                <button
                  onClick={() => handleRemoveLink(link.id)}
                  className="hover:text-error text-outline ml-1"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Live SQL Preview Box & Buttons */}
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1 bg-surface-container-lowest rounded-lg border border-outline-variant/20 p-2 font-mono text-xs text-on-surface-variant overflow-x-auto whitespace-pre">
            <code>{generatedSql}</code>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => {
                if (onExecuteSql) {
                  onExecuteSql(generatedSql);
                } else if (onNavigateTab) {
                  onNavigateTab("sql");
                }
              }}
              className="px-3.5 py-2 rounded-lg bg-surface-container-high border border-outline-variant/30 text-on-surface hover:bg-surface-variant text-xs font-medium flex items-center gap-1.5 transition"
            >
              <span className="material-symbols-outlined text-[16px] text-tertiary">terminal</span>
              <span>Open in SQL Studio</span>
            </button>

            <button
              disabled={isSaving || tables.length === 0}
              onClick={handleSaveJoinedCheckpoint}
              className="px-3.5 py-2 rounded-lg bg-tertiary text-on-tertiary hover:opacity-90 disabled:opacity-50 text-xs font-semibold flex items-center gap-1.5 transition"
            >
              <span className="material-symbols-outlined text-[16px]">save</span>
              <span>{isSaving ? "Materializing..." : "Save Joined Version"}</span>
            </button>

            <button
              onClick={() => {
                if (onSendToChat) {
                  onSendToChat(
                    `Analyze the relational relationship between the mapped tables using this join:\n\`\`\`sql\n${generatedSql}\n\`\`\``
                  );
                }
                if (onNavigateTab) {
                  onNavigateTab("canvas");
                }
              }}
              className="px-3.5 py-2 rounded-lg bg-primary text-on-primary hover:opacity-90 text-xs font-semibold flex items-center gap-1.5 transition"
            >
              <span className="material-symbols-outlined text-[16px]">smart_toy</span>
              <span>Ask AI Analyst</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
