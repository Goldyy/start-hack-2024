"use client"

import {OvoHunter} from '@/lib/interfaces/ovo-hunter'
import { ColumnDef } from '@tanstack/react-table'
import { DataTable } from '../shadcn/data-table'
import {Checkbox} from "@/components/ui/checkbox"

import { MoreHorizontal } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import { deleteOvoHunter } from '@/lib/data/model/ovo-hunter'

const columns: ColumnDef<OvoHunter>[] = [
    {
        header: "ID",
        accessorKey: "id"
    },
    {
        header: "Name",
        accessorKey: "name"
    },
    {
        header: "Impressed by",
        accessorKey: "is_impressed_by"
    },
    {
        header: "Nickname",
        accessorKey: "nickname"
    },
    {
        header: "Created At",
        accessorKey: "created_at"
    },
    {
        id: "actions",
        cell: ({ row }) => {
          const ovoHunter = row.original
     
          return (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-8 w-8 p-0">
                  <span className="sr-only">Open menu</span>
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>Actions</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                    onClick={() => deleteOvoHunter(ovoHunter.id)}
                >
                    delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )
        },
      },
]

export default function OvoHuntersTable({
    data,
}: {
    data: OvoHunter[]
}) {
    return (
        <DataTable
            columns={columns}
            data={data}
        />
    )
}