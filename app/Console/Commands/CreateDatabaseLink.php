<?php
namespace App\Console\Commands;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;

class CreateDatabaseLink extends Command
{
    protected $signature = 'app:link:database';
    protected $description = 'Create a symbolic link to the database directory';

    public function handle()
    {
        $target = base_path('database/database.sqlite');
        $link = base_path('scraper/database.sqlite');
        
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