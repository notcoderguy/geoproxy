<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;

class CreateMmdbLink extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:link:mmdb';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create a symbolic link to the mmdb directory';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Link proxy to the api directory
        $target = storage_path('app/private/geoip');
        $link = base_path('scraper/mmdb');

        // Check if target exists
        if (!file_exists($target)) {
            $this->error("The target [$target] does not exist.");
            return;
        }

        // Ensure target directory exists (though it should since target exists)
        $targetDir = dirname($target);
        if (!file_exists($targetDir)) {
            if (!File::makeDirectory($targetDir, 0755, true)) {
                $this->error("Failed to create target directory [$targetDir]");
                return;
            }
        }

        // Ensure link directory exists
        $linkDir = dirname($link);
        if (!file_exists($linkDir)) {
            if (!File::makeDirectory($linkDir, 0755, true)) {
                $this->error("Failed to create link directory [$linkDir]");
                return;
            }
        }

        // Remove existing link if it exists
        if (file_exists($link)) {
            $this->info("The link [$link] already exists. It will be overwritten.");
            if (!File::delete($link)) {
                $this->error("Failed to delete existing link [$link]");
                return;
            }
        }

        // Create the symbolic link
        if (!File::link($target, $link)) {
            $this->error("Failed to create the link [$link]");
            return;
        }

        $this->info("The link [$link] has been created successfully.");
        $this->info("The target [$target] is linked to [$link].");
    }
}
